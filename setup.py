from cx_Freeze import setup, Executable

bdist_msi_options = {
    'upgrade_code': '{5fa7309a-bb70-42bb-bb83-6b1ee24f5026}',
    'add_to_path': True,
    'initial_target_dir': r'[ProgramFilesFolder]\%s' % ("mchell")
    }

build_exe_options = {
    'includes': ['atexit'],
    'include_files': ["schemas/"]
    }

target = Executable(
    script="mchell.py",
    icon="icon.ico"
    )

setup(name = "Mchell" ,
      version = "1.0.0",
      description = "A Bedrock mcfunction shell and interpreter" ,
      executables = [target],
      options={
          'bdist_msi': bdist_msi_options,
          'build_exe': build_exe_options})