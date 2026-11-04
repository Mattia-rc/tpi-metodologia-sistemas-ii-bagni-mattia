class ErrorSolicitud(Exception):
    """Error previsto del caso de uso, con un mensaje público estable."""
    def __init__(self, mensaje, status=400):
        super().__init__(mensaje)
        self.status = status
