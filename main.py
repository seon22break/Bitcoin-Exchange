from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
import requests
import json


class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []

        r = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        data_string = json.loads(r.content)

        if event.get_keyword() == "sbtc":

            self.getDataStatus(items, data_string)

        elif event.get_keyword() == "usd":

            cantidad = event.get_argument()
            result = (float(cantidad) * 0.0000206326)
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name='%s BTC' % result,
                                             description='The result is a aproximated',
                                             on_enter=HideWindowAction()))

        elif event.get_keyword() == "eur":

            cantidad = event.get_argument()
            result = (float(cantidad) * 0.0000249802)
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name='%s BTC' % result,
                                             description='The result is a aproximated',
                                             on_enter=HideWindowAction()))

        return RenderResultListAction(items)

    # Get data to API JSON

    def getDataStatus(self, items, data_string):
        eur = data_string["bpi"]["EUR"]["rate"]
        dollar = data_string["bpi"]["USD"]["rate"]
        update = data_string['time']['updated']

        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name='EUR: %s' % str(eur),
                                         description='Last Update: %s' % update,
                                         on_enter=HideWindowAction()))
        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name='DOLLAR: %s' % str(dollar),
                                         description='Last Update: %s' % update,
                                         on_enter=HideWindowAction()))

        return items


if __name__ == '__main__':
    DemoExtension().run()
