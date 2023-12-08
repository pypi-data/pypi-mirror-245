from . import ConfController, PrintController, Response
import json

class Gateway:

    _erro = ''

    def __init__(self, token):

        self._token = token
        self._response = Response()

    def execute(self):

        self._message = {'token': self._token}
        self._response.send_message(json.dumps(self._message))
        result = self._response.get_message()
        print(result)

        if result == 'getprinters':

            self._search_printers()
            self._message['erro'] = self._erro
            self._response.send_message(self._message)
            self._response.close()

    def _change_config(self):
        
        self._message = {'token': self._token}
        self._response.send_message(json.dumps(self._message))
        self._message = self._response.get_message()
        self._conf = ConfController(json.loads(self._message))
        self._conf.execute()

    def _search_printers(self):

        try:
            self._print = PrintController()
            self._message = self._print.get_printer_list(self._token)
        except:
            self._erro = 'Não foi possível encontrar impressoras!'

    def _print_cupom_fiscal(self):

        self._message = {'token': self._token}
        self._response.send_message(json.dumps(self._message))
        self._message = self._response.get_message()
        self._print = PrintController()
        self._print.print_data(json.loads(self._message))

    def _emitir_nota_fiscal(self):

        self._message = {'token': self._token}
        self._response.send_message(json.dumps(self._message))
        self._message = self._response.get_message()