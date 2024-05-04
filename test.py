from pathlib import Path
from string import Template



path = Path('D:\PYTHON\discod\\18plus\photos\\')
photo18plus = (sum(1 for x in path.glob('*') if x.is_file())) 
photo18plus_size = sum(f.stat().st_size for f in path.glob('**/*') if f.is_file())
 
path = Path('D:\PYTHON\discod\\18plus\\video_files\\')
video18plus = (sum(1 for x in path.glob('*') if x.is_file())) 

template = """
Tổng photo 18+ : $photo18plus file - $photo18plus_size byte\n
Tổng video 18+ : $video18plus file \n
"""

prine = Template(template).substitute(photo18plus=photo18plus,video18plus=video18plus, photo18plus_size = photo18plus_size)

print(prine)