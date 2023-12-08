""" Module to find, install and setup software packages
    J. Bregeon, L. Arrabito
    15/09/2019
"""

__RCSID__ = "$Id$"

# generic imports
import os
import glob
import shutil
import tarfile

# DIRAC imports
import DIRAC
from DIRAC.DataManagementSystem.Client.DataManager import DataManager

# from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from CTADIRAC.Core.Utilities.tool_box import get_os_and_cpu_info


class SoftwareManager:
    """Manage software setup"""

    def __init__(self, soft_category):
        """Constructor"""
        self.CVMFS_DIR = "/cvmfs/sw.cta-observatory.org/software"
        self.LFN_ROOT = "/vo.cta.in2p3.fr/software"
        self.SOFT_CATEGORY_DICT = soft_category
        self.dm = DataManager()

    def _search_software(self, package, version, compiler):
        """Look for sotfware package"""
        # software package category
        category = self.SOFT_CATEGORY_DICT[package]
        # look for software on cvmfs
        package_dir = os.path.join(
            self.CVMFS_DIR, "centos7", compiler, category, package, version
        )
        if os.path.isdir(package_dir):
            DIRAC.gLogger.notice(
                f"Found package {package} version {version} at:\n{package_dir}"
            )
            return DIRAC.S_OK({"Source": "cvmfs", "Path": package_dir})
        else:
            DIRAC.gLogger.notice(f"{package_dir}\n not found on cvmfs")
            # look for tarball in the Dirac file catalog
            package_dir = os.path.join(
                self.LFN_ROOT, "centos7", compiler, category, package, version
            )
            DIRAC.gLogger.notice(f"Looking for tarball in {package_dir}")
            results = self.dm.getFilesFromDirectory(package_dir)
            try:
                first_file_path = results["Value"][0]
                if first_file_path[-7:] == ".tar.gz":
                    results = self.dm.getActiveReplicas(first_file_path)
                    if results["OK"]:
                        return DIRAC.S_OK({"Source": "tarball", "Path": package_dir})
            except BaseException:
                DIRAC.gLogger.warn("No usual tarball found in the directory")

        return DIRAC.S_ERROR(
            f"Could not find package {package} / {version} / {compiler} in any location"
        )

    def find_software(self, package, version, compiler="gcc48_default"):
        """check if the software package is installed in any software area
        Keyword arguments:
        package -- package name as the directory name
        version -- software version as the directory name
        compiler -- compiler version and configuration
        """
        # first check if cvmfs is available
        # Not used anymore -> First try cvmfs and then try tarball
        # ops_helper = Operations()
        # use_cvmfs = ops_helper.getValue('SoftwarePolicy/UseCvmfs', bool)
        # DIRAC.gLogger.notice('SoftwarePolicy for UseCvmfs is:', use_cvmfs)

        # get platform and cpu information
        try:
            platform, cpu_name, inst = get_os_and_cpu_info()
            DIRAC.gLogger.notice(f"Running {platform} on {cpu_name} ({inst})")
        except BaseException:
            inst = "noOpt"
            DIRAC.gLogger.notice("Could not determine platform and cpu information")

        req_inst = compiler.split("_")[1]
        if req_inst == "default":
            results = self._search_software(package, version, compiler)
            return results
        elif req_inst == "noOpt":
            results = self._search_software(package, version, compiler)
            return results
        elif req_inst == "sse4":
            if inst in ["sse4", "avx", "avx2"]:
                results = self._search_software(package, version, compiler)
                return results
            else:
                DIRAC.gLogger.warn(
                    "CPU has no sse4 instructions, running non optimized version"
                )
                match_compiler = compiler.replace(req_inst, "noOpt")
                results = self._search_software(package, version, match_compiler)
                return results
        elif req_inst == "avx":
            if inst in ["avx", "avx2"]:
                results = self._search_software(package, version, compiler)
                return results
            else:
                DIRAC.gLogger.warn(
                    "CPU has no avx instructions, running non optimized version"
                )
                match_compiler = compiler.replace(req_inst, "noOpt")
                results = self._search_software(package, version, match_compiler)
                return results
        elif req_inst == "avx2":
            if inst in ["avx2"]:
                results = self._search_software(package, version, compiler)
                return results
            else:
                DIRAC.gLogger.warn(
                    "CPU has no avx2 instructions, running non optimized version"
                )
                match_compiler = compiler.replace(req_inst, "noOpt")
                results = self._search_software(package, version, match_compiler)
                return results
        elif compiler == "gcc83_avx512":
            if inst in ["avx512"]:
                results = self._search_software(package, version, compiler)
                return results
            else:
                DIRAC.gLogger.warn(
                    "CPU has no avx512 instructions, running non optimized version"
                )
                match_compiler = compiler.replace(req_inst, "noOpt")
                results = self._search_software(package, version, match_compiler)
                return results
        elif req_inst == "matchcpu":
            match_compiler = compiler.replace(req_inst, inst)
            if match_compiler == "gcc48_avx512":
                DIRAC.gLogger.warn(f"{inst} not available for gcc48")
                DIRAC.gLogger.warn("Using gcc83 avx512 instead")
                match_compiler = "gcc83_avx512"
            results = self._search_software(package, version, match_compiler)
            return results
        else:
            DIRAC.S_ERROR(f"Unknown compiler specified: {compiler}")
        return DIRAC.S_ERROR(
            "Could not find package %s version %s / %s in any location"
            % (package, version, compiler)
        )

    def install_dirac_scripts(self, package_dir):
        """copy DIRAC scripts in the current directory"""
        dirac_scripts = glob.glob(os.path.join(package_dir, "dirac_*"))
        try:
            for one_file in dirac_scripts:
                shutil.copy2(one_file, ".")
            return DIRAC.S_OK()
        except shutil.Error as error:
            return DIRAC.S_ERROR(f"Failed to install DIRAC scripts:\n{error}")

    def dump_setup_script_path(self, package_dir, textfilename="setup_script_path.txt"):
        """dump the path to setupPackage.sh in a one line ascii file
        to be read and source by the following script
        """
        script_path = os.path.join(package_dir, "setupPackage.sh")
        open(textfilename, "w").writelines(script_path + "\n")
        return DIRAC.S_OK()

    def install_software(self, tar_lfn, target_dir="."):
        """install software package in the current directory"""
        DIRAC.gLogger.notice(f"Installing package at {tar_lfn}")

        # Download the tar file
        DIRAC.gLogger.notice("Trying to download package:", tar_lfn)
        res = self.dm.getFile(tar_lfn)
        if not res["OK"]:
            return res

        if tar_lfn in res["Value"]["Successful"]:
            DIRAC.gLogger.notice(" Package downloaded successfully:", tar_lfn)
        else:
            error = "Failed to download package:", tar_lfn
            return DIRAC.S_ERROR(error)

        # Extract the tar file to the target directory
        tar_mode = "r|*"
        tar = tarfile.open(os.path.basename(tar_lfn), tar_mode)
        for tarInfo in tar:
            tar.extract(tarInfo, target_dir)
        tar.close()
        os.unlink(os.path.basename(tar_lfn))
        # Done
        DIRAC.gLogger.notice(
            f"Package {tar_lfn} installed successfully at:\n{target_dir}"
        )

        return DIRAC.S_OK(target_dir)
