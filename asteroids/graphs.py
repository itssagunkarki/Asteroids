import pandas as pd
import plotly
import plotly.express as px
import json


class AsteroidGraph():
    def __init__(self, asteroids_data: json):
        self.asteroids_data = asteroids_data
        self.graph = {}
        self.get_violin_num_ast()

    def get_graph(self) -> dict:
        return self.graph
    
    def _get_near_earth_objects(self, unit:str ='meters') -> pd.DataFrame:
        """
        returns a dataframe with the id and min and max diameter of the asteroid
        """
        ast_diameter = []
        for i in self.asteroids_data['near_earth_objects'].keys():
            for j in self.asteroids_data['near_earth_objects'][i]:
                ast_diameter.append({'id': j['id'], 'diameter': j['estimated_diameter'][unit]})

        dfx = pd.DataFrame(ast_diameter)
        dfx = pd.concat([dfx['id'], pd.json_normalize(dfx['diameter'])], axis=1)
        return dfx

    
    def get_violin_num_ast(self) -> None:
        """
        returns a violin plot of the average diameter of the asteroids
        """
        dfx = self._get_near_earth_objects()

        dfx['average_diameter'] = (dfx['estimated_diameter_max'] + dfx['estimated_diameter_min']) / 2

        fig = px.violin(dfx, y='average_diameter',
                box=True,  # Include box plot
                points='all',  # Display individual data points
                hover_data=dfx.columns)

        fig.update_layout(
        yaxis_title="Average Diameter (meters)",
        font=dict(size=12),  # Adjust the font size
        plot_bgcolor='white',  # Set the background color
        margin=dict(l=40, r=40, t=60, b=40)  # Adjust the plot margins
        )


        # convert it to JSON and add to graph
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        self.graph['size_ast_violin_graph'] = graphJSON



    


