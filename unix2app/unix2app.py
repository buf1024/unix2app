import os.path
import shutil

import click
import yaml

plist = """<?xml version="1.0" ?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>CFBundleDevelopmentRegion</key>
        <string>zh_CN</string>
        
        <key>CFBundleDisplayName</key>
        <string></string>
    
        <key>CFBundleExecutable</key>
        <string>{executable}</string>
    
        <key>CFBundleIconFile</key>
        <string>{icon}</string>
    
        <key>CFBundleIdentifier</key>
        <string>{identifier}</string>
    
        <key>CFBundleInfoDictionaryVersion</key>
        <string>6.0</string>
        
        <key>CFBundleName</key>
        <string>{name}</string>
    
        <key>CFBundlePackageType</key>
        <string>APPL</string>
    
        <key>NSPrincipalClass</key>
        <string>NSApplication</string>
        <key>NSHighResolutionCapable</key>
        <string>True</string>
    
        <key>CFBundleShortVersionString</key>
        <string>{version}</string>
    
        <key>CFBundleSignature</key>
        <string>{signature}</string>
    
        <key>CFBundleVersion</key>
        <string>{build_version}</string>
    
        <key>NSHumanReadableCopyright</key>
        <string>{copyright}</string>
    </dict>
</plist>
"""


def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(path, mode)


def build_directory(output):
    os.makedirs(output, True)
    os.makedirs(os.path.join(output, 'Contents'), True)
    os.makedirs(os.path.join(output, 'Contents', 'MacOS'), True)
    os.makedirs(os.path.join(output, 'Contents', 'PlugIns'), True)
    os.makedirs(os.path.join(output, 'Contents', 'Resources'), True)
    os.makedirs(os.path.join(output, 'Contents', 'Resources', 'zh-Hans.lproj'), True)


def write_pkginfo(path):
    with open(path, 'w') as f:
        f.write('APPL????')


def write_plist(path, conf_dict):
    info_plist = plist.format(
        executable=conf_dict['executable'],
        icon=conf_dict['icon'],
        identifier=conf_dict['identifier'],
        name=conf_dict['name'][:-4],
        version=conf_dict['version'],
        signature=conf_dict['signature'],
        build_version=conf_dict['build'],
        copyright=conf_dict['copyright']
    )

    with open(path, 'w') as f:
        f.write(info_plist)


def copy_file(src, dst):
    try:
        shutil.copy2(src, dst)
    except OSError:
        shutil.copy(src, dst)


def copy_files(src, dest, conf_dict):
    files = os.listdir(src)
    for f in files:
        if not os.path.isfile(f):
            continue
        if f.endswith('.dylib') or f.endswith('.d') or f.endswith('.rlib') or f in conf_dict['executables']:
            if f == conf_dict['executable']:
                make_executable(os.path.join(src, f))
            copy_file(os.path.join(src, f), os.path.join(dest, 'Contents', 'MacOS'))
            continue
        copy_file(os.path.join(src, f), os.path.join(dest, 'Contents', 'Resources'))


@click.command()
@click.option('--config', default='build.yml', type=str, help='Configure file.')
@click.option('--output', default='out', type=str, help='Output dir, default ./output')
@click.option('--rm/--no-rm', default=False, help='Remove output dir first or not')
@click.argument('execute', default=None, type=str, required=False)
def main(output='out', config='build.yml', rm=False, execute=None):
    """
    configure yml
    name: egui
    executable: bc
    version: '2.3.2'
    build: r11
    identifier: com.toyent.com
    icon: a.icon
    signature: ????
    copyright: 'copyright (c) 2022 buf1024'
    """
    executables = None
    if execute is not None:
        executables = execute.split(',')
    conf_dict = dict(
        name='{}.app'.format(execute),
        executable=execute,
        executables=executables,
        identifier='com.toyent.{}'.format(execute),
        version='0.0.1',
        build='1',
        icon=None,
        signature='????',
        copyright='copyright (c) 2022 buf1024'
    )
    if os.path.exists(config):
        with open(config) as f:
            c = yaml.load(f.read(), yaml.FullLoader)
            if 'executable' in c and c['executable'] is not None:
                c['executables'] = c['executable'].split(',')
            conf_dict.update(c)

    if conf_dict['name'] is None or \
            conf_dict['executable'] is None or not os.path.exists(conf_dict['executable']):
        print('entry executable file "{}" not exists'.format(conf_dict['executable']))
        return

    if not conf_dict['name'].endswith('.app'):
        conf_dict['name'] = '{}.app'.format(conf_dict['name'])

    if rm and os.path.exists(output):
        shutil.rmtree(output)

    out_app = os.path.join(output, conf_dict['name'])
    build_directory(out_app)
    write_pkginfo(os.path.join(out_app, 'Contents', 'PkgInfo'))
    write_plist(os.path.join(out_app, 'Contents', 'Info.plist'), conf_dict)
    copy_files('.', out_app, conf_dict)
    print('write: \n{}'.format(yaml.dump(conf_dict)))


if __name__ == '__main__':
    main()
