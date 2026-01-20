{
  pkgs ? import <nixpkgs> {
    overlays = [
      (import (fetchTarball "https://github.com/oxalica/rust-overlay/archive/master.tar.gz"))
    ];
  },
}:

let

  rustToolchain = pkgs.rust-bin.stable.latest.default.override {
    extensions = [
      "rust-src"
      "rust-analyzer"
    ];
  };

  # https://github.com/NixOS/nixpkgs/blob/nixos-unstable/pkgs/development/python-modules/pygls/default.nix#L66
  pygls = pkgs.python3Packages.buildPythonPackage rec {
    pname = "pygls";
    version = "2.0.0";
    pyproject = true;

    src = pkgs.fetchFromGitHub {
      owner = "openlawlibrary";
      repo = "pygls";
      tag = "v${version}";
      hash = "sha256-dQLK18EACiN+DpWp81Vgaan0mwtifhrmH4xwkqttKvg=";
    };

    nativeBuildInputs = [ pkgs.python3Packages.poetry-core ];

    propagatedBuildInputs = with pkgs.python3Packages; [
      attrs
      cattrs
      lsprotocol_2025
    ];

    optional-dependencies = {
      ws = [ pkgs.python3Packages.websockets ];
    };

    nativeCheckInputs = with pkgs.python3Packages; [
      pytest-asyncio
      pytestCheckHook
    ];

    # Fixes hanging tests on Darwin
    __darwinAllowLocalNetworking = true;

    preCheck = pkgs.lib.optionalString pkgs.stdenv.hostPlatform.isDarwin ''
      # Darwin issue: OSError: [Errno 24] Too many open files
      ulimit -n 1024
    '';

    pythonImportsCheck = [ "pygls" ];

    meta = {
      description = "Pythonic generic implementation of the Language Server Protocol";
      homepage = "https://github.com/openlawlibrary/pygls";
      changelog = "https://github.com/openlawlibrary/pygls/blob/${version}/CHANGELOG.md";
      license = pkgs.lib.licenses.asl20;
      maintainers = with pkgs.lib.maintainers; [ kira-bruneau ];
    };
  };

  python = pkgs.python3.withPackages (
    ps: with ps; [
      pygls
      pyyaml
    ]
  );
in

pkgs.mkShell {
  buildInputs = with pkgs; [
    uv
    rustToolchain
    cmake
    pkg-config
    openssl
    dbus
  ];
  nativeBuildInputs = with pkgs; [
    pkg-config
  ];

  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath (
    with pkgs;
    [
      openssl
      dbus
      libgcc
    ]
  );
  shellHook = ''
        export PYTHONPATH=${python}/${python.sitePackages}

        export UV_NO_MANAGED_PYTHON=1
        export UV_SYSTEM_PYTHON=1
        export UV_NO_SYNC=1

        mkdir -p .helix

        cat > .helix/languages.toml << EOF
    [language-server.ty]
    command = "ty"
    args = ["server"]

    [language-server.ty.config]
    completions.autoImport = true
    EOF
        cat > ty.toml << EOF
    [environment]
    python = "${python}"
    [rules]
    possibly-unbound-attribute = "ignore"
    possibly-missing-attribute = "ignore"
    EOF
  '';
}
