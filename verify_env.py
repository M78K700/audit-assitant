import sys
import pkg_resources
import importlib

def check_package(package_name, required_version=None):
    try:
        module = importlib.import_module(package_name)
        if required_version:
            installed_version = pkg_resources.get_distribution(package_name).version
            print(f"✓ {package_name} {installed_version} is installed")
            if installed_version != required_version:
                print(f"  Warning: Version mismatch. Required: {required_version}, Installed: {installed_version}")
        else:
            print(f"✓ {package_name} is installed")
        return True
    except ImportError:
        print(f"✗ {package_name} is not installed")
        return False

def main():
    print("Python Environment Verification")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print("\nChecking required packages:")
    
    required_packages = {
        'streamlit': '1.32.0',
        'pandas': '2.2.0',
        'numpy': '1.26.3',
        'plotly': '5.18.0',
        'reportlab': '4.1.0',
        'Pillow': '10.2.0'
    }
    
    all_installed = True
    for package, version in required_packages.items():
        if not check_package(package, version):
            all_installed = False
    
    print("\nChecking additional dependencies:")
    additional_packages = [
        'click', 'rich', 'jinja2', 'google.protobuf', 'grpcio',
        'altair', 'pyarrow', 'markdown', 'tornado', 'werkzeug',
        'cachetools', 'gitpython', 'pydeck', 'validators', 'semver'
    ]
    
    for package in additional_packages:
        if not check_package(package):
            all_installed = False
    
    if all_installed:
        print("\n✓ All required packages are installed")
    else:
        print("\n✗ Some packages are missing or have incorrect versions")
        print("Please run: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 