project('ppm2',
        ['c', 'fortran'],
        version: '0.0.0',
        meson_version: '>= 1.3.0',
)

py = import('python').find_installation(pure: true)

fortran_sources = files(
  'opm.f', 'min.f', 'rmsd.f', 'solva.f', 'readpdb.f',
  'read_small.f', 'watface.f', 'tilting.f', 'locate.f',
  'profile.f', 'hbcor.f', 'deftm.f', 'orient.f', 'find_segm.f'
)

install_subdir(
    'src/ppm2',
    install_dir: py.get_install_dir(pure: true)
)

executable('immers',
  fortran_sources,
  install: true,
  fortran_args: ['-O', '-g'],
  install_dir: py.get_install_dir() / 'ppm2/_bin',
)
