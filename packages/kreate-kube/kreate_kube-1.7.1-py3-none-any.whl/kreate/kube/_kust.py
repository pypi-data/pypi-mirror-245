import logging

from ..kore import JinYamlKomponent, Module, App, KomponentKlass
from .resource import Resource, MultiDocumentResource
from .patch import Patch, CustomPatch

logger = logging.getLogger(__name__)


class KustomizeModule(Module):
    def init_app(self, app: App) -> None:
        app.register_klass(CustomPatch)

    def kreate_app_komponents(self, app: App):
        for res in app.komponents:
            if isinstance(res, Resource):
                self.kreate_embedded_patches(app, res)

    def kreate_embedded_patches(self, app: App, res: Resource) -> None:
        if "patches" in res.strukture:
            for patch_name in sorted(res.strukture.get("patches").keys()):
                subpatches = res.strukture.get_path(f"patches.{patch_name}")
                klass = res.app.klasses[patch_name]
                if not subpatches.keys():
                    subpatches = {"main": {}}
                # use sorted because some patches, e.g. the MountVolumes
                # result in a list, were the order can be unpredictable
                for shortname in sorted(subpatches.keys()):
                    Patch.from_target(app, klass, shortname, target_id=res.id)


class Kustomization(JinYamlKomponent):
    def resources(self):
        return [
            res
            for res in self.app.komponents
            if isinstance(res, Resource) or isinstance(res, MultiDocumentResource)
        ]

    def patches(self):
        return [res for res in self.app.komponents if isinstance(res, Patch)]

    def var(self, cm: str, varname: str):
        value = self.strukture.get_path(f"configmaps.{cm}.vars.{varname}")
        if not isinstance(value, str):
            value = self.app.konfig.get_path("var", {}).get(varname, None)
        if value is None:
            raise ValueError(f"var {varname} should not be None")
        return value

    def kopy_file(self, filename: str) -> str:
        # Note: you can not usu the full get_path, since the filename might contain a dot
        location: str = self.app.konfig.get_path("file", {}).get(filename)
        if not location:
            raise ValueError(f"Could not find file {filename} in file section to kopy")
        if location.startswith("dekrypt:"):
            target = self.app.target_path / "secrets" / "files" / filename
            result = "secrets/files/" + filename
        else:
            target = self.app.target_path / "files" / filename
            result = "files/" + filename
        self.app.konfig.file_getter.kopy_file(location, target)
        return result

    def get_filename(self):
        return "kustomization.yaml"

    def aktivate(self):
        super().aktivate()
        self.remove_vars()

    def remove_vars(self):
        removals = self.strukture.get("remove_vars", {})
        for cm_to_remove in removals:
            for cm in self.get_path("configMapGenerator", {}):
                if cm["name"] == cm_to_remove:
                    for var in self.strukture["remove_vars"][cm_to_remove]:
                        found = False
                        for idx, v in enumerate(cm["literals"]):
                            if v.startswith(var + "="):
                                found = True
                                logger.info(f"removing var {cm_to_remove}.{v}")
                                cm["literals"].pop(idx)
                        if not found:
                            logger.warning(
                                f"could not find var to remove {cm_to_remove}.{var}"
                            )
