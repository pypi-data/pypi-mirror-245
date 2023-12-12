# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import dash_bootstrap_components as dbc
import uuid

from dash_extensions.enrich import html


class ActorStatisticsTableAIO(html.Div):

    class ids:
        pass

    ids = ids

    def __init__(self, data: dict, aio_id: str = None):
        """ActorStatisticsTableAIO is an All-in-One component that is composed
        of multiple components which are not exposed but only configured internally.

        - `data` - Data to be displayed in the datatable component.
        - `aio_id` - The All-in-One component ID used to generate the table components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        self._style: dict = {
            "textAlign": "left",
            "fontSize": 12,
            "fontFamily": "Roboto",
            "color": "rgba(0, 0, 0, 1)",
            "backgroundColor": "rgba(255, 255, 255, 0)"
        }

        table_data = self.to_dash(data)

        super().__init__([
            html.H5("Actor Statistics", className="card-title"),
            html.Hr(className="my-2"),
            dbc.Card(
                [
                    dbc.CardBody(
                        table_data,
                        className="border-0 bg-transparent"
                    ),
                ],
                className="border-0 bg-transparent"
            )
        ])

    def to_dash(self, data: dict) -> list:

        table_data = []

        for key, values in data.items():
            columns = [
                dbc.Col(
                    html.Label(
                        key if key != "Header" else "",
                        style = self._style
                    ),
                    width=2
                ),
            ]
            for value in values:
                columns.append(
                    dbc.Col(
                        html.Label(
                            value,
                            style = self._style
                        ),
                        width=2
                    ),
                )

            table_data.append(dbc.Row(columns))

        return table_data
