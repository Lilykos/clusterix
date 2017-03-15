from pandasql import sqldf
from ..config import log
from ..utils import load_df

to_float = lambda l: [float(i) for i in l]


@log('- Search started.')
def search(query):
    results = sqldf('SELECT clx_id FROM df WHERE {} ;'.format(query),
                    {'df': load_df()}).values
    return [int(i[0]) for i in results]


def get_node_details(_id):
    df = load_df()
    fields = df[df['clx_id'] == _id].columns.values
    details = [detail[:20] for detail in df[df['clx_id'] == _id].values[0]
               if isinstance(detail, str)]
    return fields, details


def get_field_data(fields):
    df = load_df()
    fields += ['clx_id', 'clx_cluster']
    return [dict(zip(fields, to_float(row)))
            for row in df[fields].values]
