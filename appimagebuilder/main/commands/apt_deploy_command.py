#  Copyright  2021 Alexis Lopez Zubieta
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
from pathlib import Path

from appimagebuilder.builder.deploy.apt import Deploy, Venv
from appimagebuilder.main.commands.deploy_command import DeployCommand


class AptDeployCommand(DeployCommand):
    def __init__(
        self,
        app_dir: str,
        cache_dir: str,
        deploy_record: {},
        packages: [str],
        exclude: [str] = None,
        architectures: [str] = None,
        sources: [str] = None,
        keys: [str] = None,
        allow_unauthenticated: str = None,
    ):
        super().__init__("apt deploy", app_dir, cache_dir, deploy_record)
        self.packages = packages
        self._exclude = exclude
        self._allow_unauthenticated = allow_unauthenticated
        self._keys = keys
        self._sources = sources
        self._architectures = architectures

    def id(self):
        return "apt-deploy"

    def __call__(self, *args, **kwargs):
        apt_venv = self._setup_apt_venv()

        apt_deploy = Deploy(apt_venv)

        deployed_packages = apt_deploy.deploy(
            self.packages, self._app_dir, self._exclude
        )

        self.deploy_record["apt"] = {
            "sources": apt_venv.sources,
            "packages": deployed_packages,
        }

    def _setup_apt_venv(self):
        apt_options = {
            "APT::Get::AllowUnauthenticated": self._allow_unauthenticated,
            "Acquire::AllowInsecureRepositories": self._allow_unauthenticated,
        }
        apt_venv = Venv(
            str(Path(self._cache_dir) / "apt"),
            self._sources,
            self._keys,
            self._architectures,
            apt_options,
        )
        return apt_venv
