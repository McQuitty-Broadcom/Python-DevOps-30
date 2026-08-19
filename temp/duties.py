import sys; sys.path.append('./')

from duty import duty
from zowesupport import *

# Commands to Run

    
@duty
def run(ctx):
    """Run Bind and Grant Jobs"""
    dataset = ""
    submitJobAndDownloadOutput(ctx, dataset, "job-archive", 0)

@duty
def build_cobol(ctx):
    """Build Cobol Element"""
    command = ""
    simpleCommand(ctx, command, "output")

@duty
def build_lnk(ctx):
    """Build LNK Element"""
    command = ""
    simpleCommand(ctx, command, "output")

@duty
def build(ctx):
    """Build the application"""
    build_cobol(ctx)
    build_lnk(ctx)

@duty
def clean(ctx):
    """Clean up temp files"""
    ctx.run("rm -rf endevor*.txt output")
