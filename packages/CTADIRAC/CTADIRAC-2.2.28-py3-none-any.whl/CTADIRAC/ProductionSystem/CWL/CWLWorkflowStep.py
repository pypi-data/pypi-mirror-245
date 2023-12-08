"""
    Class to handle a workflow step described in CWL and composed of a commandLineTool
"""

__RCSID__ = "$Id$"

import schema_salad
from ruamel.yaml  import YAML
yaml = YAML(typ='safe', pure=True)
import copy
from cwltool.load_tool import load_tool
from cwltool.context import LoadingContext, RuntimeContext
import cwltool.process
import cwltool.main
from CTADIRAC.ProductionSystem.CWL.CWLUtils import (
    check_if_file_input,
    add_fake_file,
    maybe_quote,
)


class WorkflowStep:
    """Composite class for workflow step (production step + job)"""

    def __init__(self):
        """Constructor"""
        self.command_line = ""
        self.process = None
        self.inputs = None
        self.sources = []
        self.sources_outputs = []

    def replace_step_input_by_source_output(self, step_input, source_output):
        if (source_output["type"] == "File") or (source_output["type"] == "Directory"):
            inp_class = source_output["type"]
            inp_location = source_output["outputBinding"]["glob"]
            self.inputs[step_input] = yaml.comments.CommentedMap(
                {"class": inp_class, "location": inp_location}
            )

    def add_source_output_to_tool_input(self, source_output):
        if (source_output["type"] == "File") or (source_output["type"] == "Directory"):
            inp_class = source_output["type"]
            inp_id = cwltool.process.shortname(source_output["_tool_entry"]["id"])
            inp_location = source_output["outputBinding"]["glob"]
            self.inputs[inp_id] = yaml.comments.CommentedMap(
                {"class": inp_class, "location": inp_location}
            )

    def load(self, input_cwl, input_yaml, sources=None, sources_outputs=None):
        loader = schema_salad.ref_resolver.Loader(
            {"@base": input_yaml, "path": {"@type": "@id"}}
        )
        self.inputs, _ = loader.resolve_ref(input_yaml)

        if sources:
            # Replace input by the output of the source
            for inp in sources:
                step_input = cwltool.process.shortname(inp["id"])
                for out in sources_outputs:
                    if out["id"] == inp["source"]:
                        self.replace_step_input_by_source_output(step_input, out)

        loading_context = LoadingContext({"strict": False, "debug": True})
        self.process = load_tool(input_cwl, loading_context)

    def get_command_line(self, sources=None, sources_outputs=None):
        """Get command line from a CommandLineTool description"""

        for entry in self.inputs.values():
            if check_if_file_input(entry):
                add_fake_file(entry["location"])

        for inp in self.process.tool["inputs"]:
            if cwltool.process.shortname(inp["id"]) in self.inputs:
                pass
            elif (
                cwltool.process.shortname(inp["id"]) not in self.inputs
                and "default" in inp
            ):
                self.inputs[cwltool.process.shortname(inp["id"])] = copy.copy(
                    inp["default"]
                )
            elif (
                cwltool.process.shortname(inp["id"]) not in self.inputs
                and inp["type"][0] == "null"
            ):
                pass
            else:
                raise Exception(
                    f"Missing inputs `{cwltool.process.shortname(inp['id'])}`"
                )

        runtime_context = RuntimeContext()

        if sources:
            for out in sources_outputs:
                self.add_source_output_to_tool_input(out)

        for job in self.process.job(self.inputs, None, runtime_context):
            for i in range(len(job.builder.bindings)):
                if isinstance(
                    job.builder.bindings[i]["datum"], dict
                ):  # replace file path by its location
                    if "location" in job.builder.bindings[i]["datum"]:
                        path = job.builder.bindings[i]["datum"]["path"]
                        location = job.builder.bindings[i]["datum"]["location"]
                        for k in range(len(job.command_line)):
                            if path in job.command_line[k]:
                                job.command_line[k] = job.command_line[k].replace(
                                    path, location
                                )
            self.command_line = " ".join([maybe_quote(arg) for arg in job.command_line])

        #    for entry in self.inputs.values():
        #        if check_if_file_input(entry):
        #            remove_fake_file(entry["location"])
        return self
