from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
from pyflink.table import StreamTableEnvironment
from pyflink.datastream.connectors.file_system import FileSource, StreamFormat
from pyflink.common import WatermarkStrategy
import re

env = StreamExecutionEnvironment.get_execution_environment()
env.set_runtime_mode(RuntimeExecutionMode.BATCH)
env.set_parallelism(1)  

t_env = StreamTableEnvironment.create(env)

ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

ds = env.from_source(source=FileSource.for_record_stream_format(StreamFormat.text_line_format(), 'SSH.log')
    .process_static_file_set().build(),
    watermark_strategy=WatermarkStrategy.for_monotonous_timestamps(),
    source_name="file_source")

result = (
    ds.filter(lambda value: 'Invalid user' in value)
    .flat_map(lambda value: [ip for ip in ip_pattern.findall(value)])
    .map(lambda ip: (ip.split('.')[0], 1))  
    .key_by(lambda x: x[0])  
    .sum(lambda x: int(x[1]))  
)

def categorize_ip_range(ip):
    first_octet = int(ip[0])
    if 0 <= first_octet <= 49:
        return 'Range 1'
    elif 50 <= first_octet <= 99:
        return 'Range 2'
    elif 100 <= first_octet <= 149:
        return 'Range 3'
    elif 150 <= first_octet <= 199:
        return 'Range 4'
    elif 200 <= first_octet <= 249:
        return 'Range 5'
    else:
        return 'Range 6'


result_with_range = result.map(lambda ip, count: (categorize_ip_range(ip), count))

t_env.from_data_stream(result_with_range, ['Range', 'Count']).to_pandas().print()
