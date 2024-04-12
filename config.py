import os


def get_drives():
    drives = []
    for drive in range(ord('A'), ord('Z') + 1):
        drive_letter = chr(drive) + ':\\'
        if os.path.exists(drive_letter):
            drives.append(drive_letter)
    return drives


class Config:
    drives = get_drives()
    base_folder = "./StormLand"
    apps_database = f"{base_folder}/apps_db.db"
    scan_folder = base_folder + "/"
    scan_data = scan_folder + "data/"
    main_scan_data_file = scan_data + "StormApps.db"
    scan_logs = scan_folder + "logs/"
    extensions_to_track = [".exe", ".lnk", ".bat", ".cmd", ".com", ".ps1"]
    text_extensions = [
        '.dib', '.asc', '.dsl', '.ftc', '.lisp', '.numbers', '.template', '.uop', '.raw', '.uot', '.bash_profile',
        '.emlx', '.hdp', '.jsonld', '.tcz', '.ans', '.webp', '.mj2', '.php', '.mjp', '.rwz', '.text', '.rwl',
        '.json', '.dng', '.pef', '.xml', '.odb', '.bas', '.log', '.config', '.jpx', '.pod', '.bsh', '.db',
        '.xquery', '.raf', '.x3f', '.rtf', '.sgml', '.azw8', '.otp', '.webloc', '.drf', '.opml', '.ts', '.lst',
        '.tab', '.sti', '.vdf', '.uos', '.fb2', '.bmp', '.lit', '.txtz', '.3fr', '.c', '.xsl', '.bash_logout',
        '.fodp', '.md', '.sas', '.tpl', '.sub', '.odp', '.r', '.gml', '.kfx', '.xslt', '.eps', '.nrw', '.wdp',
        '.s', '.docx', '.doc', '.bash_history', '.jpm', '.html', '.ics', '.mobi', '.ots', '.psd', '.nt', '.make',
        '.pdb', '.dwg', '.ksh', '.nq', '.srf', '.js', '.gtp', '.hpp', '.dml', '.awk', '.tsv', '.stata', '.lrc',
        '.j2c', '.mbox', '.tcl', '.pmlz', '.pages', '.chm', '.erf', '.ott', '.tif', '.mml', '.azw', '.kc2',
        '.gif', '.jif', '.n3', '.odm', '.crw', '.dxf', '.8bps', '.f', '.texinfo', '.rb', '.jpg', '.m4', '.epub',
        '.mbx', '.k25', '.pm', '.odg', '.j2k', '.hcard', '.icns', '.ttl', '.odf', '.mht', '.pas', '.nfo', '.sxg',
        '.txt', '.imp', '.msg', '.owl', '.tiff', '.jpc', '.trig', '.cfg', '.plaintext', '.t3z', '.diz', '.jp2',
        '.mef', '.sed', '.aspx', '.jfi', '.htaccess', '.inf', '.cr2', '.mdc', '.paf', '.env', '.sami', '.sql',
        '.keynote', '.8bim', '.texz', '.sxm', '.res', '.ptx', '.fodt', '.jsp', '.java', '.azw3', '.ps1', '.nef',
        '.emlxpart', '.tex', '.h', '.webvtt', '.sbv', '.cpp', '.vmt', '.std', '.sxd', '.jpeg', '.css', '.srw',
        '.for', '.envrc', '.mos', '.lrf', '.inputrc', '.oft', '.sh', '.mm', '.bash_aliases', '.cdr', '.inc',
        '.svg', '.properties', '.dcr', '.fods', '.mhtml', '.cap', '.bashrc', '.indd', '.jfif', '.ssa', '.rtfd',
        '.xhtml', '.srt', '.odt', '.sr2', '.csh', '.asm', '.bat', '.asp', '.sma', '.stw', '.dds', '.shtml', '.ai',
        '.eml', '.ass', '.rw2', '.cur', '.ico', '.markdown', '.sparql', '.arw', '.yml', '.dtd', '.wsdl', '.vtt',
        '.rq', '.ods', '.sxi', '.mfw', '.dcs', '.oxps', '.py', '.note', '.vbs', '.eip', '.ftn', '.rc', '.yaml',
        '.bash_login', '.j6i', '.vcf', '.fo', '.spr', '.sxw', '.xsd', '.m', '.jpe', '.tir', '.stc', '.vcard',
        '.jpf', '.sc', '.cgi', '.cr3', '.cvs', '.xps', '.svgz', '.orf', '.zsh', '.kf8', '.tga', '.kdc', '.cpt',
        '.rdf', '.odi', '.jxr', '.key', '.ini', '.pdf', '.fff', '.conf', '.pdd', '.fodg', '.qtk', '.ciff',
        '.pxn', '.pml', '.ps', '.iiq', '.csv', '.mrw', '.odc', '.azw4', '.pl', '.r3d', '.png'
    ]
