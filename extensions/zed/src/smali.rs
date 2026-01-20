use zed_extension_api as zed;
use zed_extension_api::{settings::LspSettings, LanguageServerId, Result};

struct SmaliExtension;

impl SmaliExtension {
    fn smalisp_binary(&self, _language_server_id: &LanguageServerId, worktree: &zed::Worktree) -> Result<zed::Command> {
        let mut args = Vec::new();

        if let Ok(LspSettings {
            binary: Some(binary),
            ..
        }) = LspSettings::for_worktree("smalisp", worktree)
        {
            if let Some(arg_settings) = binary.arguments {
                args.extend(arg_settings);
            }

            if let Some(path) = binary.path {
                let (platform, _) = zed::current_platform();
                let environment = match platform {
                    zed::Os::Mac | zed::Os::Linux => worktree.shell_env(),
                    zed::Os::Windows => Vec::new(),
                };
                return Ok(zed::Command {
                    command: path.clone(),
                    args,
                    env: environment,
                });
            }
        }

        if let Some(path) = worktree.which("smalisp") {
            let (platform, _) = zed::current_platform();
            let environment = match platform {
                zed::Os::Mac | zed::Os::Linux => worktree.shell_env(),
                zed::Os::Windows => Vec::new(),
            };
            return Ok(zed::Command {
                command: path,
                args,
                env: environment,
            });
        }

        Err(format!(
            "smalisp binary not found. Please ensure smalisp is installed and available in PATH, or specify the path in Zed settings."
        ).into())
    }
}

impl zed::Extension for SmaliExtension {
    fn new() -> Self {
        Self
    }

    fn language_server_command(
        &mut self,
        language_server_id: &LanguageServerId,
        worktree: &zed::Worktree,
    ) -> Result<zed::Command> {
        self.smalisp_binary(language_server_id, worktree)
    }
}

zed::register_extension!(SmaliExtension);
