import sys; sys.path.append('./')

from duty import duty
from zowesupport import *

# Commands to Run

    
@duty
def run(ctx):
    """Run Bind and Grant Jobs"""
    dataset = "echo run job"
    submitJobAndDownloadOutput(ctx, dataset, "output/job-archive", 0)

@duty
def build_cobol(ctx):
    """Build Cobol Element"""
    command = "echo build cobol"
    simpleCommand(ctx, command, "output")

@duty
def build_lnk(ctx):
    """Build LNK Element"""
    command = "echo build lnk"
    simpleCommand(ctx, command, "output")

@duty
def clean(ctx):
    """Clean up temp files"""
    ctx.run("rm -rf endevor*.txt output")
