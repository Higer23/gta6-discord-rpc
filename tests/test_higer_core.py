import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).parents[1]/"src"))
from gta6_rpc.timer import parse_duration
from gta6_rpc.config import build_config
from gta6_rpc.validation import validate_config
from gta6_rpc.presence import PresenceBuilder
from gta6_rpc.models import PresenceState
class CoreTests(unittest.TestCase):
 def base(self):return {"client_id":"123","played_time":{"hours":1,"minutes":2,"seconds":3},"update_interval":1,"activity_rotation":{"enabled":True,"min_seconds":60,"max_seconds":120},"assets":{"large_image":"gta6"},"buttons":[],"activities":["Explore"],"locations":["Vice City"],"details_suffixes":["Free Roam"]}
 def test_duration(self):self.assertEqual(parse_duration("127:43:29"),127*3600+43*60+29)
 def test_invalid_rotation(self):
  d=self.base();d["activity_rotation"]["min_seconds"]=200;d["activity_rotation"]["max_seconds"]=100;self.assertTrue(validate_config(build_config(d)))
 def test_payload(self):self.assertEqual(PresenceBuilder(build_config(self.base())).build(PresenceState(10,100,"Explore","Vice City","Free Roam"))["start"],100)
if __name__=="__main__":unittest.main()
