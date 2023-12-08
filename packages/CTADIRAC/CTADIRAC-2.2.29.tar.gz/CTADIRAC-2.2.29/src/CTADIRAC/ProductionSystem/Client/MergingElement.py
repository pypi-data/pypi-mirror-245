"""
   Wrapper around the job class to build a workflow element (production step + job)
"""

__RCSID__ = "$Id$"

# generic imports
from copy import deepcopy
import json

# DIRAC imports
from CTADIRAC.Interfaces.API.CtapipeMergeJob import CtapipeMergeJob
from CTADIRAC.ProductionSystem.Client.WorkflowElement import WorkflowElement


class MergingElement(WorkflowElement):
    """Composite class for workflow element (production step + job)"""

    #############################################################################

    def __init__(self, parent_prod_step):
        """Constructor"""
        WorkflowElement.__init__(self, parent_prod_step)
        self.job = CtapipeMergeJob(cpuTime=259200.0)
        self.job.setOutputSandbox(["*Log.txt"])
        self.job.input_limit = None
        self.job.merged = 0
        self.prod_step.Type = "Merging"
        self.prod_step.Name = "Merging"
        self.mandatory_keys = {"MCCampaign", "configuration_id", "version"}
        self.mandatory_job_config_keys = {"output_extension"}
        self.constrained_job_keys = {"catalogs", "group_size", "moon"}
        self.constrained_input_keys = {
            "pointing_dir",
            "zenith_angle",
            "sct",
            "moon",
            "div_ang",
        }
        self.file_meta_fields = {"nsb", "div_ang", "split"}

    def set_constrained_job_attribute(self, key, value):
        """Set job attribute with constraints"""
        if key == "catalogs":
            # remove whitespaces between catalogs if there are some and separate between commas
            setattr(self.job, key, json.dumps(value.replace(", ", ",").split(sep=",")))
        elif key == "group_size":
            setattr(self.job, key, value)
            self.prod_step.GroupSize = self.job.group_size
        elif key == "moon":
            if value == "dark":
                self.job.output_file_metadata["nsb"] = 1
            elif value == "half":
                self.job.output_file_metadata["nsb"] = 5
            elif value == "full":
                self.job.output_file_metadata["nsb"] = 19

    def set_constrained_input_query(self, key, value):
        """Set input meta query with constraints"""
        if key == "pointing_dir":
            if value == "North":
                self.prod_step.Inputquery["phiP"] = 180
            elif value == "South":
                self.prod_step.Inputquery["phiP"] = 0
        elif key == "zenith_angle":
            self.prod_step.Inputquery["thetaP"] = float(value)
        elif key == "sct":
            self.prod_step.Inputquery["sct"] = str(value)
        elif key == "moon":
            if value == "dark":
                self.prod_step.Inputquery["nsb"] = 1
            elif value == "half":
                self.prod_step.Inputquery["nsb"] = 5
            elif value == "full":
                self.prod_step.Inputquery["nsb"] = 19
        elif key == "div_ang":
            self.prod_step.Inputquery["div_ang"] = str(value)

    def build_job_output_data(self, workflow_step):
        """Build job output meta data"""
        metadata = deepcopy(self.prod_step.Inputquery)
        for key, value in workflow_step["job_config"].items():
            metadata[key] = value
        merged = self.get_merging_level()
        metadata["merged"] = merged
        self.job.set_output_metadata(metadata)

    def get_merging_level(self):
        """Get the merging level from parent step or from the user query"""
        if self.prod_step.ParentStep:
            merged = self.prod_step.ParentStep.Outputquery["merged"]
        else:
            merged = self.job.merged
        return merged

    def build_element_config(self):
        """Set job and production step attributes specific to the configuration"""
        self.prod_step.GroupSize = self.job.group_size
        self.job.set_executable_sequence(debug=False)
        self.prod_step.Body = self.job.workflow.toXML()

    #############################################################################
