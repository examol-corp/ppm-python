project('ppm2',
        ['c', 'fortran'],
        version: '0.0.0',
        meson_version: '>= 1.3.0',
)

py = import('python').find_installation(pure: false)

fortran_sources = files(
  'opm.f', 'min.f', 'rmsd.f', 'solva.f', 'readpdb.f',
  'read_small.f', 'watface.f', 'tilting.f', 'locate.f',
  'profile.f', 'hbcor.f', 'deftm.f', 'orient.f', 'find_segm.f'
)

# Modern & reliable way: let Meson handle the extension naming
immers = py.extension_module('immers',
  fortran_sources,
  install: true,
  subdir: 'ppm2',
  fortran_args: ['-O', '-g'],
)

py.install_sources(
    ['src/ppm2/__init__.py', 'src/ppm2/__main__.py'],
    subdir: 'ppm2'
)
executable('immers',
  fortran_sources,
  install: true,
  fortran_args: ['-O', '-g'],
  install_dir: py.get_install_dir() / 'ppm2/_bin',
)
