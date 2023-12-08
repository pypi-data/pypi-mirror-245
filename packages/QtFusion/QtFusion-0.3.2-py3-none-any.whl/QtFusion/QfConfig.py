# QtFusion, AGPL-3.0 license

class QF_Config:
    VERBOSE = True

    @classmethod
    def set_verbose(cls, mode=True):
        """
        Set the qtfusion verbose.

        Args:
            mode (bool): If QTFUSION_VERBOSE is True, print the information.
        """
        # User can set the verbose mode before using the package
        cls.VERBOSE = mode
