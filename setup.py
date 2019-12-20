from cx_Freeze import setup, Executable

bdist_msi_options = {
    'upgrade_code': '{5fa7309a-bb70-42bb-bb83-6b1ee24f5026}',
    'add_to_path': True,
    'initial_target_dir': r'[ProgramFilesFolder]\%s' % ("mcf"),
    }

build_exe_options = {
    'includes': ['atexit'],
    }

target = Executable(
    script="mcf.py",
    icon="icon.ico"
    )


setup(name = "MCF" ,
      version = "0.1" ,
      description = "" ,
      executables = [target],
      options={
          'bdist_msi': bdist_msi_options,
          'build_exe': build_exe_options})