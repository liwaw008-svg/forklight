import hashlib
from conftest import CONTRACT

EVIDENCE=['https://archive.example/policy','https://lab.example/model','https://review.example/assessment']
BODIES=[b'Controlled evidence forecasts a measurable benefit.',b'Model comparison supports the intervention.',b'Review identifies manageable downside risk.']
FIELDS=['Adopt the proposed night-bus service redesign.','Keep the current fixed late-night schedule.','Use demand-responsive routing after midnight.','Average rider wait time across the service area.','The first twelve weeks after launch.']

def prepared(direct_vm,direct_deploy,direct_alice):
    direct_vm.sender=direct_alice; contract=direct_deploy(CONTRACT)
    contract.seal('night-bus',*FIELDS,EVIDENCE)
    for host,body in zip(('archive.example','lab.example','review.example'),BODIES): direct_vm.mock_web(host.replace('.',r'\.'),{'status':200,'body':body.decode()})
    direct_vm.mock_llm(r'.*Forklight counterfactual.*','{"path":"ACT","confidence":"HIGH","baseline_score":42,"intervention_score":71,"supporting":[0,1],"opposing":[2]}')
    direct_vm.mock_llm(r'.*Forklight forecast verifier.*','{"valid":true}')
    return contract

def test_forecast_binds_scores_indexes_and_digests(direct_vm,direct_deploy,direct_alice):
    contract=prepared(direct_vm,direct_deploy,direct_alice); contract.illuminate('NIGHT-BUS'); result=contract.get_forecast('night-bus')
    assert result['stage']=='FORKED' and result['path']=='ACT' and result['intervention_score']==71
    assert result['supporting']==[0,1] and result['forecast_digests']==[hashlib.sha256(x).hexdigest() for x in BODIES]

def test_duplicate_origins_and_ids_fail(direct_vm,direct_deploy,direct_alice):
    contract=prepared(direct_vm,direct_deploy,direct_alice)
    with direct_vm.expect_revert('complete three-origin forecast required'): contract.seal('night-bus',*FIELDS,EVIDENCE)
    with direct_vm.expect_revert('complete three-origin forecast required'): contract.seal('other',*FIELDS,[EVIDENCE[0],EVIDENCE[0]+'?copy=1',EVIDENCE[2]])

def test_validator_rejects_forged_attribution(direct_vm,direct_deploy,direct_alice):
    contract=prepared(direct_vm,direct_deploy,direct_alice); result=contract._project(contract.forecasts['NIGHT-BUS'])
    assert direct_vm.run_validator(leader_result=result) is True
    forged=dict(result); forged['intervention_score']=12
    assert direct_vm.run_validator(leader_result=forged) is False
    forged=dict(result); forged['digests']=list(reversed(result['digests']))
    assert direct_vm.run_validator(leader_result=forged) is False

def test_independent_observation_and_calibration(direct_vm,direct_deploy,direct_alice):
    contract=prepared(direct_vm,direct_deploy,direct_alice); contract.illuminate('night-bus')
    with direct_vm.expect_revert('independent two-origin observation required'): contract.observe('night-bus','Wait time improved across measured routes.',['https://archive.example/new','https://audit.example/result'])
    observation=['https://transit.example/result','https://audit.example/result']
    contract.observe('night-bus','Median wait time fell by nine minutes across the measured routes.',observation)
    direct_vm.mock_web(r'transit\.example',{'status':200,'body':'Published route-level wait-time data.'}); direct_vm.mock_web(r'audit\.example',{'status':200,'body':'Independent audit confirms the direction.'})
    direct_vm.mock_llm(r'.*Forklight calibration.*','{"outcome":"BETTER","calibration":"ACCURATE"}')
    direct_vm.mock_llm(r'.*Forklight calibration verifier.*','{"valid":true}')
    contract.calibrate('night-bus'); closed=contract.get_forecast('night-bus')
    assert closed['stage']=='CLOSED' and closed['outcome']=='BETTER' and closed['calibration']=='ACCURATE'
