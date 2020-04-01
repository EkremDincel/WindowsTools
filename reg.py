import winreg as _winreg

def set_reg_util(root, path, name, value):
    try:
##        _winreg.CreateKey(root, path)
        registry_key = _winreg.OpenKey(root, path, 0, 
                                       _winreg.KEY_WRITE)
        _winreg.SetValueEx(registry_key, name, 0, _winreg.REG_SZ, value)
        _winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False

def get_reg_util(root, path, name):
    try:
        registry_key = _winreg.OpenKey(root, path, 0,
                                       _winreg.KEY_READ)
        value, regtype = _winreg.QueryValueEx(registry_key, name)
        _winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None

def get_reg(path, name):
    root, path = path.split("\\", 1)
    root = getattr(_winreg, root)
    return get_reg_util(root, path, name)

def set_reg(path, name, value):
    root, path = path.split("\\", 1)
    root = getattr(_winreg, root)
    return set_reg_util(root, path, name, value)
