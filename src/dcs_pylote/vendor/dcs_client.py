import subprocess
import os
import shutil
import uuid
from enum import Enum, auto

DEFAULT_DCS_PATH = os.path.join("E:\\", "Program Files", "DCS World OpenBeta", "bin", "DCS.exe")
DEFAULT_DCS_REFERENCE_DIR = os.path.join("D:\\", "Saved Games", "DCS.openbeta")

class DCSLaunchMode(Enum):
    NORMAL = auto()
    HEADLESS = auto()
    SERVER = auto()

class DCSClient:
    def __init__(self, dcs_path=DEFAULT_DCS_PATH, mode=DCSLaunchMode.NORMAL, mission_file=None, reference_dir=DEFAULT_DCS_REFERENCE_DIR, run_as_admin=False, instance_id=None):
        """
        Initialize the DCSClient.

        :param dcs_path: Path to DCS World executable.
        :param mission_file: Optional path to a mission file to launch.
        :param mode: Launch mode (NORMAL, HEADLESS, SERVER).
        :param reference_dir: Directory to copy essential DCS configuration from.
        :param run_as_admin: If True, launch DCS with administrator privileges.
        :param instance_id: Custom instance ID. If None, generates a unique ID.
        """
        self.dcs_path = dcs_path
        self.mode = mode
        self.mission_file = mission_file
        self.reference_dir = reference_dir
        self.run_as_admin = run_as_admin
        
        # Generate unique instance ID for this client
        self.instance_id = instance_id or f"dcs_{uuid.uuid4().hex[:8]}"
        self.write_dir = f"DCS Pylotes/{self.instance_id}"  # Organized under DCS Pylotes
        
        self.process = None
        
        print(f"Created DCS client with instance ID: {self.instance_id}")
        
        # Pre-setup the config if we can determine the full path
        self._setup_config_if_possible()


    def launch(self):
        """
        Launch DCS World, optionally with a mission file.
        """
        
        cmd = [self.dcs_path]
        
        # Add command line arguments to bypass launcher
        if self.mode == DCSLaunchMode.HEADLESS:
            cmd.extend([
                "--norender",         # Start in server mode (no GUI dialogs)
            ])
        elif self.mode == DCSLaunchMode.SERVER:
            cmd.extend([
                "--server",         # Start in server mode (no GUI dialogs)
            ])

        # Add custom write directory if specified
        if self.write_dir:
            cmd.extend(["-w", self.write_dir])
        
        if self.mission_file:
            cmd.append(self.mission_file)
        
        print(f"Launching DCS with command: {' '.join(cmd)}")
        print(f"Write directory: {self.write_dir}")
                
        self.process = subprocess.Popen(cmd)
        return self.process
    
    def _setup_config_if_possible(self):
        """
        Try to setup the config directory and copy Options.lua before launch.
        """
        # Try to determine where DCS will create the directory
        # This is usually in the user's Saved Games folder
        instance_path = os.path.join(DEFAULT_DCS_REFERENCE_DIR, "..", self.write_dir)
        config_path = os.path.join(instance_path, "Config")
        
        try:
            # Create the directory structure
            os.makedirs(instance_path, exist_ok=True)
            os.makedirs(config_path, exist_ok=True)
            print(f"  ✓ Created instance directory: {instance_path}")
            print(f"  ✓ Created config directory: {config_path}")

            # Copy appSettings.lua
            self._copy_app_settings(config_path)
            
            # Copy the minimal Options.lua
            self._copy_minimal_options(config_path)
            # self._copy_reference_options(config_path)
            
            # Copy authdata.bin from main DCS directory
            self._copy_authdata(config_path)

            # Copy shader directories
            self._copy_shader_dirs(instance_path)
            
        except Exception as e:
            print(f"  ! Could not pre-setup config: {e}")
            print(f"  DCS will create directory structure when it starts")

    def _copy_minimal_options(self, config_path):
        """
        Copy minimal Options.lua to the config directory.
        """
        # Get the path to the Options.lua file in our project
        current_dir = os.path.dirname(os.path.abspath(__file__))
        options_source = os.path.join(current_dir, "Options.lua")
        options_dest = os.path.join(config_path, "options.lua")
        
        if os.path.exists(options_source):
            shutil.copy2(options_source, options_dest)
            print(f"  ✓ Copied Options.lua to: {options_dest}")
        
    def _copy_app_settings(self, config_path):
        """
        Copy appSettings.lua to the config directory.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_settings_source = os.path.join(current_dir, "appSettings.lua")
        app_settings_dest = os.path.join(config_path, "appSettings.lua")

        if os.path.exists(app_settings_source):
            shutil.copy2(app_settings_source, app_settings_dest)
            print(f"  ✓ Copied appSettings.lua to: {app_settings_dest}")
    
    def _copy_reference_options(self, config_path):
        """
        Copy Options.lua from the reference DCS directory's Config folder.
        """
        options_source = os.path.join(self.reference_dir, "Config", "Options.lua")
        options_dest = os.path.join(config_path, "Options.lua")
        if os.path.exists(options_source):
            try:
                shutil.copy2(options_source, options_dest)
                print(f"  ✓ Copied Options.lua from reference directory: {options_source}")
            except Exception as e:
                print(f"  ! Failed to copy Options.lua: {e}")
        else:
            print(f"  ! Options.lua not found at: {options_source}")
            print(f"    Check that the reference directory is correct: {self.reference_dir}")

    def _copy_authdata(self, config_path):
        """
        Copy authdata.bin from the reference DCS directory.
        """
        authdata_source = os.path.join(self.reference_dir, "Config", "authdata.bin")
        
        if os.path.exists(authdata_source):
            authdata_dest = os.path.join(config_path, "authdata.bin")
            try:
                shutil.copy2(authdata_source, authdata_dest)
                print(f"  ✓ Copied authdata.bin from: {authdata_source}")
            except Exception as e:
                print(f"  ! Failed to copy authdata.bin: {e}")
        else:
            print(f"  ! authdata.bin not found at: {authdata_source}")
            print(f"    Check that the reference directory is correct: {self.reference_dir}")


        network_vault_source = os.path.join(self.reference_dir, "Config", "network.vault")
        if os.path.exists(network_vault_source):
            network_vault_dest = os.path.join(config_path, "network.vault")
            try:
                shutil.copy2(network_vault_source, network_vault_dest)
                print(f"  ✓ Copied network.vault from: {network_vault_source}")
            except Exception as e:
                print(f"  ! Failed to copy network.vault: {e}")
        else:
            print(f"  ! network.vault not found at: {network_vault_source}")
            print(f"    Check that the reference directory is correct: {self.reference_dir}")
    
    def _copy_shader_dirs(self, instance_path):
        """
        Copy 'fxo' and 'metashaders2' directories from the reference DCS directory.
        """
        for dirname in ["fxo", "metashaders2"]:
            src_dir = os.path.join(self.reference_dir, dirname)
            dest_dir = os.path.join(instance_path, dirname)
            if os.path.exists(src_dir):
                try:
                    if os.path.exists(dest_dir):
                        shutil.rmtree(dest_dir)
                    shutil.copytree(src_dir, dest_dir)
                    print(f"  ✓ Copied {dirname} directory from: {src_dir}")
                except Exception as e:
                    print(f"  ! Failed to copy {dirname}: {e}")
            else:
                print(f"  ! {dirname} directory not found at: {src_dir}")
                print(f"    Check that the reference directory is correct: {self.reference_dir}")


    def is_running(self):
        """
        Check if DCS World is still running.
        """
        return self.process and self.process.poll() is None

    def terminate(self):
        """
        Terminate the DCS World process.
        """
        if self.process and self.is_running():
            self.process.terminate()
            self.process.wait()

    def __del__(self):
        self.terminate()
