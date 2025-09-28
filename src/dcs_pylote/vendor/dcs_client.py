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
                "--norender",        # Start in headless mode (no rendering)
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
            self._copy_config(config_path)

            # Copy references from the reference directory
            self._copy_references(config_path)
            
        except Exception as e:
            print(f"  ! Could not pre-setup config: {e}")
            print(f"  DCS will create directory structure when it starts")

    def _copy_config(self, config_path):
        """
        Copy minimal Options.lua to the config directory.
        """
        # Get the path to the Options.lua file in our project
        current_dir = os.path.dirname(os.path.abspath(__file__))
        options_source = os.path.join(current_dir, "dcs_config")
        options_dest = os.path.join(config_path, "options.lua")

        files = [
            "Options.lua",
            "appSettings.lua",
            "imgui.ini"
        ]
        
        for filename in files:
            options_source = os.path.join(current_dir, "dcs_config", filename)
            options_dest = os.path.join(config_path, filename)
            if os.path.exists(options_source):
                shutil.copy2(options_source, options_dest)
                print(f"  ✓ Copied {filename} to: {options_dest}")

    def _copy_references(self, config_path):
        """
        Copy Options.lua from the reference DCS directory's Config folder.
        """
        filepaths = [
            ["Config", "authdata.bin"],
            ["Config", "network.vault"],
            ["fxo"],
            ["metashaders2"],
            ["launcher.sqlite3"]
        ]

        for filepath in filepaths:
            source_path = os.path.join(self.reference_dir, *filepath)
            if os.path.isdir(source_path):
                dest_path = os.path.join(config_path, *filepath)
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                shutil.copytree(source_path, dest_path)
                print(f"  ✓ Copied directory {filepath[-1]} from reference directory: {source_path}")
                continue
            else:
                source_path = os.path.join(self.reference_dir, *filepath)
                dest_path = os.path.join(config_path, filepath[-1])
            if os.path.exists(source_path):
                try:
                    shutil.copy2(source_path, dest_path)
                    print(f"  ✓ Copied {filepath[-1]} from reference directory: {source_path}")
                except Exception as e:
                    print(f"  ! Failed to copy {filepath[-1]}: {e}")
            else:
                print(f"  ! {filepath[-1]} not found at: {source_path}")
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
            
        # Delete the custom save directory for this client instance
        instance_path = os.path.join(DEFAULT_DCS_REFERENCE_DIR, "..", self.write_dir)
        if os.path.exists(instance_path):
            try:
                shutil.rmtree(instance_path)
                print(f"  ✓ Deleted instance directory: {instance_path}")
            except Exception as e:
                print(f"  ! Failed to delete instance directory: {e}")

    def __del__(self):
        self.terminate()
