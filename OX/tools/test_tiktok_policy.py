#!/usr/bin/env python3
"""Static configuration regression; does not test device selection or node access."""
from manage import ROOT, profile, sections

expected = 'static = TikTok, 日本, 美国, 台湾, 默认代理, direct'
for source in (profile(), (ROOT/'profiles/quantumultx.conf').read_text()):
    policies = sections(source)['[policy]']
    assert [line for line in policies if line.startswith('static = TikTok,')] == [expected]
    for region in ('日本', '美国', '台湾'):
        assert any(line.startswith(f'static = {region},') for line in policies)
    resources = sections(source)['[filter_remote]']
    assert any('/rules/TikTok.list,' in line and 'force-policy=TikTok' in line and 'enabled=true' in line for line in resources)
    assert not any('tiktok' in line.lower() for line in sections(source)['[rewrite_remote]'] if not line.startswith('#'))
print('PASS: TikTok JP/US/TW order, region references, routing binding, no TikTok rewrite. Device not tested.')
