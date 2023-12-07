import traceback
from win32com.client import Dispatch
from photoshop_object_model import PhotoshopObjectModel
from photoshop_object_model.application import Application

class PhotoshopSession(PhotoshopObjectModel):
    """
    This class is used to run code in photoshop using the Photoshop Object Model
    It is designed to be used as a context : 

    >>> with PhotoshopSession() as ps:
    >>>     print(ps.Application.Version)
    >>>     new_layer = ps.Application.ActiveDocument.ArtLayers.Add()
    >>>     new_layer.Name = "Hello World"
    """
    def __init__(
            self,
            error_popup:bool=True,
            error_message:str="The script execution encountered some errors",
            success_popup:bool=True,
            success_message:str="The script was successfully executed",
        ):
        super().__init__()
        self.error_popup = error_popup
        self.success_popup = success_popup
        self.error_message = error_message
        self.success_message = success_message
        self.Application:Application = Dispatch("Photoshop.Application")
    
    def __enter__(self):
        return self
    
    def __exit__(self, _err_type, _err_value, _traceback):
        """
        Depending on whether or not the code was successfully executed, show an alert in photoshop
        """
        if _err_value and self.error_popup:
            ps_err_message = (eval(str(_err_value))[2][2])
            py_traceback = traceback.format_exc()
            py_traceback = py_traceback.replace("\\", "\\\\")
            py_traceback = py_traceback.replace("\n", "\\n")
            py_traceback = py_traceback.replace("\"", "\\\"")
            self.Application.DoJavaScript(f"""
                var message = File.decode("{self.error_message}");
                var err_value = File.decode("{ps_err_message}");
                var err_traceback = File.decode("{py_traceback}");
                alert(message + " :\\n" + err_value + "\\n\\n" + err_traceback, "Error", true);
            """
            )
        elif self.success_popup:
            self.Application.DoJavaScript(f"""
                var message = File.decode("{self.success_message}");
                alert(message, "Success", false);
            """
            )

if __name__ == "__main__":
    with PhotoshopSession() as ps:
        print(ps.Application.Version)