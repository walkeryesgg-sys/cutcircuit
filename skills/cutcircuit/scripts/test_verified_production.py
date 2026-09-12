"""Synthetic structural regressions; fixtures are NOT evidence of audiovisual quality."""
import copy
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from validate_timeline import validate
from validate_release import validate as release


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='cutcircuit-contract-')
        cls.base = Path(cls.temp.name)
        def ffmpeg(*args):
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error',*args],check=True)
        ffmpeg('-f','lavfi','-i','sine=frequency=440:duration=1',str(cls.base/'voice.wav'))
        ffmpeg('-f','lavfi','-i','color=c=blue:s=160x90:r=30:d=3','-c:v','libx264',str(cls.base/'picture.mp4'))
        (cls.base/'review.md').write_text('SYNTHETIC TEST ONLY. Does not establish speech, picture fitness or full watch.')
        audio_hash = hashlib.sha256((cls.base/'voice.wav').read_bytes()).hexdigest()
        cls.data = dict(mode='audio_first_rebuild',duration=2.3,caption_renderer='one',visible_caption_layers=['one'],baked_caption_sources=[],units=[],captions=[],shots=[dict(unit_ids=['u1','u2'],start=0,end=2.3,kind='footage',file='picture.mp4',picture_reason='synthetic fixture',review_evidence='review.md',source_start=0,source_duration=3,clarity_pass=True,embedded_captions=False)])
        for i,text in enumerate(['开始。','结束。']):
            key='u'+str(i+1)
            receipt=dict(audio_sha256=audio_hash,text_sha256=hashlib.sha256(text.encode()).hexdigest(),trim_start=0,trim_end=1,asr_text=text,review_status='verified',review_evidence='review.md')
            (cls.base/(key+'.json')).write_text(json.dumps(receipt))
            cls.data['units'].append(dict(id=key,text=text,start=i*1.3,end=i*1.3+1,audio='voice.wav',audio_sha256=audio_hash,provider='synthetic-fixture',voice_id='tone-not-speech',generation_evidence='review.md',binding_review=key+'.json',source_duration=1,trim_start=0,trim_end=1,audible_start=0,audible_end=1))
            cls.data['captions'].append(dict(unit_id=key,text=text[:-1],start=i*1.3,end=i*1.3+1))

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_timeline_cases(self):
        self.assertEqual(validate(self.data,self.base),[])
        def gap(d):
            d['units'][1].update(start=3,end=4)
        cases={
            'double captions':lambda d:d.update(visible_caption_layers=['one','two']),
            'burned captions':lambda d:d.update(baked_caption_sources=['old.mp4']),
            'voice gap':gap,
            'missing ID':lambda d:d['units'][0].pop('id'),
            'stale audio':lambda d:d['units'][0].update(audio_sha256='0'*64),
            'fake duration':lambda d:d['units'][0].update(source_duration=900),
            'not audio':lambda d:d['units'][0].update(audio='review.md'),
            'wrong receipt':lambda d:d['units'][0].update(binding_review='u2.json'),
            'no picture':lambda d:d.update(shots=[]),
            'uncovered tail':lambda d:d.update(duration=20),
            'uncovered intro':lambda d:d['shots'][0].update(start=.1),
            'infinite duration':lambda d:d.update(duration=float('inf')),
            'string time':lambda d:d['units'][0].update(start='0'),
        }
        for name,mutate in cases.items():
            with self.subTest(name=name):
                data=copy.deepcopy(self.data);mutate(data)
                self.assertTrue(validate(data,self.base),name)
        for value in (None, [], dict(asr_text='完全不同的句子')):
            (self.base/'invalid.json').write_text(json.dumps(value))
            data=copy.deepcopy(self.data);data['units'][0]['binding_review']='invalid.json'
            self.assertTrue(validate(data,self.base))

    def test_release_hash_and_watch(self):
        (self.base/'timeline.json').write_text(json.dumps(self.data))
        def item(name):
            return dict(file=name,sha256=hashlib.sha256((self.base/name).read_bytes()).hexdigest())
        data=dict(candidate=item('picture.mp4'),script=item('review.md'),timeline=item('timeline.json'),score=9.8,fatal_issues=[],reviewer=dict(id='synthetic-independent-fixture',independent=True),full_watch=dict(completed=True,playback_rate=1,perceived_modalities=['video','audio'],candidate_sha256=item('picture.mp4')['sha256']),evidence={k:'review.md' for k in ['watch_notes','voice_provenance','boundary_audition','automated_checks','semantic_shot_review']})
        self.assertEqual(release(data,self.base),[])
        stale=copy.deepcopy(data);stale['candidate']['sha256']='0'*64
        self.assertTrue(release(stale,self.base))
        no_watch=copy.deepcopy(data);no_watch['full_watch']['perceived_modalities']=['video']
        self.assertTrue(release(no_watch,self.base))
        low=copy.deepcopy(data);low['score']=9.7
        self.assertTrue(release(low,self.base))


if __name__ == '__main__':
    unittest.main(verbosity=2)
