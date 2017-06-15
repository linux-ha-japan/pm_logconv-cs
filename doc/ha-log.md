# Pacemakerログ解析支援ツール（ha-log の例）

- [変換の例 (1)](#変換の例-1)
  - [ノードpm01の ha-log](#変換の例-1--ノードpm01の-ha-log)
  - [ノードpm02の ha-log](#変換の例-1--ノードpm02の-ha-log)
- [変換の例 (2)](#変換の例-2)
  - [ノードpm01の ha-log](#変換の例-2--ノードpm01の-ha-log)
  - [ノードpm02の ha-log](#変換の例-2--ノードpm02の-ha-log)

## 変換の例 (1)
### 変換の例 (1) ： ノードpm01の ha-log
```
	Apr 24 06:19:55 pm01 pgsql(prmPg)[4974]: INFO: PostgreSQL is down
③	Apr 24 06:19:55 pm01 crmd[3594]:    info: Result of monitor operation for prmPg on pm01: 7 (not running)
	Apr 24 06:19:55 pm01 cib[3589]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/82)
	Apr 24 06:19:55 pm01 cib[3589]:    info: Diff: --- 0.4.16 2
	Apr 24 06:19:55 pm01 cib[3589]:    info: Diff: +++ 0.4.17 (null)
	Apr 24 06:19:55 pm01 cib[3589]:    info: +  /cib:  @num_updates=17
	Apr 24 06:19:55 pm01 cib[3589]:    info: ++ /cib/status/node_state[@id='3232261507']/lrm[@id='3232261507']/lrm_resources/lrm_resource[@id='prmPg']:  <lrm_rsc_op id="prmPg_last_failure_0" operation_key="prmPg_monitor_10000" operation="monitor" crm-debug-origin="do_update_resource" crm_feature_set="3.0.11" transition-key="17:3:0:0d469cae-6312-4501-a835-dd2771dcd3f8" transition-magic="0:7;17:3:0:0d469cae-6312-4501-a835-dd2771dcd3f8" on_node="pm01" call-id="25" rc-code="7" op-status="0" interval="10000" last-rc-change="1492982395" exec-time
	Apr 24 06:19:55 pm01 cib[3589]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/crmd/82, version=0.4.17)
	Apr 24 06:19:55 pm01 crmd[3594]:    info: Transition aborted by operation prmPg_monitor_10000 'create' on pm01: Inactive graph
	Apr 24 06:19:55 pm01 crmd[3594]:    info: Updating failcount for prmPg on pm01 after failed monitor: rc=7 (update=value++, time=1492982395)
	Apr 24 06:19:55 pm01 crmd[3594]:    info: Detected action (3.17) prmPg_monitor_10000.25=not running: failed
	Apr 24 06:19:55 pm01 attrd[3592]:    info: Expanded fail-count-prmPg=value++ to 1
	Apr 24 06:19:55 pm01 attrd[3592]:    info: Setting fail-count-prmPg[pm01]: (null) -> 1 from pm01
	Apr 24 06:19:55 pm01 attrd[3592]:    info: Sent update 10 with 1 changes for fail-count-prmPg, id=<n/a>, set=(null)
	Apr 24 06:19:55 pm01 attrd[3592]:    info: Setting last-failure-prmPg[pm01]: (null) -> 1492982395 from pm01
	Apr 24 06:19:55 pm01 attrd[3592]:    info: Sent update 11 with 1 changes for last-failure-prmPg, id=<n/a>, set=(null)
	Apr 24 06:19:55 pm01 cib[3589]:    info: Forwarding cib_modify operation for section status to all (origin=local/attrd/10)
	Apr 24 06:19:55 pm01 cib[3589]:    info: Forwarding cib_modify operation for section status to all (origin=local/attrd/11)
	Apr 24 06:19:55 pm01 crmd[3594]:  notice: State transition S_IDLE -> S_POLICY_ENGINE
	Apr 24 06:19:55 pm01 cib[3589]:    info: Diff: --- 0.4.17 2
	Apr 24 06:19:55 pm01 cib[3589]:    info: Diff: +++ 0.4.18 (null)
	Apr 24 06:19:55 pm01 cib[3589]:    info: +  /cib:  @num_updates=18
	Apr 24 06:19:55 pm01 cib[3589]:    info: ++ /cib/status/node_state[@id='3232261507']/transient_attributes[@id='3232261507']/instance_attributes[@id='status-3232261507']:  <nvpair id="status-3232261507-fail-count-prmPg" name="fail-count-prmPg" value="1"/>
	Apr 24 06:19:55 pm01 cib[3589]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/attrd/10, version=0.4.18)
	Apr 24 06:19:55 pm01 attrd[3592]:    info: Update 10 for fail-count-prmPg: OK (0)
	Apr 24 06:19:55 pm01 attrd[3592]:    info: Update 10 for fail-count-prmPg[pm01]=1: OK (0)
	Apr 24 06:19:55 pm01 cib[3589]:    info: Diff: --- 0.4.18 2
	Apr 24 06:19:55 pm01 cib[3589]:    info: Diff: +++ 0.4.19 (null)
	Apr 24 06:19:55 pm01 cib[3589]:    info: +  /cib:  @num_updates=19
	Apr 24 06:19:55 pm01 cib[3589]:    info: ++ /cib/status/node_state[@id='3232261507']/transient_attributes[@id='3232261507']/instance_attributes[@id='status-3232261507']:  <nvpair id="status-3232261507-last-failure-prmPg" name="last-failure-prmPg" value="1492982395"/>
	Apr 24 06:19:55 pm01 cib[3589]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/attrd/11, version=0.4.19)
	Apr 24 06:19:55 pm01 attrd[3592]:    info: Update 11 for last-failure-prmPg: OK (0)
	Apr 24 06:19:55 pm01 attrd[3592]:    info: Update 11 for last-failure-prmPg[pm01]=1492982395: OK (0)
	Apr 24 06:19:55 pm01 crmd[3594]:    info: Transition aborted by status-3232261507-fail-count-prmPg doing create fail-count-prmPg=1: Transient attribute change
	Apr 24 06:19:55 pm01 crmd[3594]:    info: Transition aborted by status-3232261507-last-failure-prmPg doing create last-failure-prmPg=1492982395: Transient attribute change
	Apr 24 06:19:55 pm01 pengine[3593]:  notice: On loss of CCM Quorum: Ignore
	Apr 24 06:19:55 pm01 pengine[3593]:    info: Node pm02 is online
	Apr 24 06:19:55 pm01 pengine[3593]:    info: Node pm01 is online
	Apr 24 06:19:55 pm01 pengine[3593]: warning: Processing failed op monitor for prmPg on pm01: not running (7)
	Apr 24 06:19:55 pm01 pengine[3593]:    info:  Resource Group: grpPg
	Apr 24 06:19:55 pm01 pengine[3593]:    info:      prmEx#011(ocf::heartbeat:sfex):#011Started pm01
	Apr 24 06:19:55 pm01 pengine[3593]:    info:      prmFs#011(ocf::heartbeat:Filesystem):#011Started pm01
	Apr 24 06:19:55 pm01 pengine[3593]:    info:      prmIp#011(ocf::heartbeat:IPaddr2):#011Started pm01
	Apr 24 06:19:55 pm01 pengine[3593]:    info:      prmPg#011(ocf::heartbeat:pgsql):#011FAILED pm01
	Apr 24 06:19:55 pm01 pengine[3593]:    info:  Start recurring monitor (10s) for prmPg on pm01
	Apr 24 06:19:55 pm01 pengine[3593]:    info: Leave   prmEx#011(Started pm01)
	Apr 24 06:19:55 pm01 pengine[3593]:    info: Leave   prmFs#011(Started pm01)
	Apr 24 06:19:55 pm01 pengine[3593]:    info: Leave   prmIp#011(Started pm01)
	Apr 24 06:19:55 pm01 pengine[3593]:  notice: Recover prmPg#011(Started pm01)
	Apr 24 06:19:55 pm01 pengine[3593]:  notice: Calculated transition 4, saving inputs in /var/lib/pacemaker/pengine/pe-input-4.bz2
	Apr 24 06:19:55 pm01 crmd[3594]:    info: pe_calc calculation pe_calc-dc-1492982395-51 is obsolete
	Apr 24 06:19:55 pm01 pengine[3593]:  notice: On loss of CCM Quorum: Ignore
	Apr 24 06:19:55 pm01 pengine[3593]:    info: Node pm02 is online
	Apr 24 06:19:55 pm01 pengine[3593]:    info: Node pm01 is online
	Apr 24 06:19:55 pm01 pengine[3593]: warning: Processing failed op monitor for prmPg on pm01: not running (7)
	Apr 24 06:19:55 pm01 pengine[3593]:    info:  Resource Group: grpPg
	Apr 24 06:19:55 pm01 pengine[3593]:    info:      prmEx#011(ocf::heartbeat:sfex):#011Started pm01
	Apr 24 06:19:55 pm01 pengine[3593]:    info:      prmFs#011(ocf::heartbeat:Filesystem):#011Started pm01
	Apr 24 06:19:55 pm01 pengine[3593]:    info:      prmIp#011(ocf::heartbeat:IPaddr2):#011Started pm01
	Apr 24 06:19:55 pm01 pengine[3593]:    info:      prmPg#011(ocf::heartbeat:pgsql):#011FAILED pm01
	Apr 24 06:19:55 pm01 pengine[3593]:    info: prmPg has failed 1 times on pm01
	Apr 24 06:19:55 pm01 pengine[3593]: warning: Forcing prmPg away from pm01 after 1 failures (max=1)
	Apr 24 06:19:55 pm01 pengine[3593]:    info:  Start recurring monitor (10s) for prmEx on pm02
	Apr 24 06:19:55 pm01 pengine[3593]:    info:  Start recurring monitor (10s) for prmFs on pm02
	Apr 24 06:19:55 pm01 pengine[3593]:    info:  Start recurring monitor (10s) for prmIp on pm02
	Apr 24 06:19:55 pm01 pengine[3593]:    info:  Start recurring monitor (10s) for prmPg on pm02
	Apr 24 06:19:55 pm01 pengine[3593]:  notice: Move    prmEx#011(Started pm01 -> pm02)
	Apr 24 06:19:55 pm01 pengine[3593]:  notice: Move    prmFs#011(Started pm01 -> pm02)
	Apr 24 06:19:55 pm01 pengine[3593]:  notice: Move    prmIp#011(Started pm01 -> pm02)
	Apr 24 06:19:55 pm01 pengine[3593]:  notice: Recover prmPg#011(Started pm01 -> pm02)
	Apr 24 06:19:55 pm01 pengine[3593]:  notice: Calculated transition 5, saving inputs in /var/lib/pacemaker/pengine/pe-input-5.bz2
	Apr 24 06:19:55 pm01 crmd[3594]:    info: State transition S_POLICY_ENGINE -> S_TRANSITION_ENGINE
	Apr 24 06:19:55 pm01 crmd[3594]:    info: Processing graph 5 (ref=pe_calc-dc-1492982395-52) derived from /var/lib/pacemaker/pengine/pe-input-5.bz2
	Apr 24 06:19:55 pm01 crmd[3594]:  notice: Initiating stop operation prmPg_stop_0 locally on pm01
	Apr 24 06:19:55 pm01 lrmd[3591]:    info: Cancelling ocf operation prmPg_monitor_10000
④	Apr 24 06:19:55 pm01 crmd[3594]:    info: Performing key=5:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8 op=prmPg_stop_0
	Apr 24 06:19:55 pm01 lrmd[3591]:    info: executing - rsc:prmPg action:stop call_id:27
	Apr 24 06:19:55 pm01 crmd[3594]:    info: Result of monitor operation for prmPg on pm01: Cancelled
	Apr 24 06:19:56 pm01 lrmd[3591]:    info: finished - rsc:prmPg action:stop call_id:27 pid:5054 exit-code:0 exec-time:124ms queue-time:0ms
⑤	Apr 24 06:19:56 pm01 crmd[3594]:  notice: Result of stop operation for prmPg on pm01: 0 (ok)
	Apr 24 06:19:56 pm01 cib[3589]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/86)
	Apr 24 06:19:56 pm01 cib[3589]:    info: Diff: --- 0.4.19 2
	Apr 24 06:19:56 pm01 cib[3589]:    info: Diff: +++ 0.4.20 (null)
	Apr 24 06:19:56 pm01 cib[3589]:    info: +  /cib:  @num_updates=20
	Apr 24 06:19:56 pm01 cib[3589]:    info: +  /cib/status/node_state[@id='3232261507']/lrm[@id='3232261507']/lrm_resources/lrm_resource[@id='prmPg']/lrm_rsc_op[@id='prmPg_last_0']:  @operation_key=prmPg_stop_0, @operation=stop, @transition-key=5:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;5:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=27, @last-run=1492982395, @last-rc-change=1492982395, @exec-time=124
	Apr 24 06:19:56 pm01 crmd[3594]:    info: Action prmPg_stop_0 (5) confirmed on pm01 (rc=0)
	Apr 24 06:19:56 pm01 crmd[3594]:  notice: Initiating stop operation prmIp_stop_0 locally on pm01
	Apr 24 06:19:56 pm01 lrmd[3591]:    info: Cancelling ocf operation prmIp_monitor_10000
	Apr 24 06:19:56 pm01 crmd[3594]:    info: Performing key=13:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8 op=prmIp_stop_0
	Apr 24 06:19:56 pm01 lrmd[3591]:    info: executing - rsc:prmIp action:stop call_id:29
	Apr 24 06:19:56 pm01 crmd[3594]:    info: Result of monitor operation for prmIp on pm01: Cancelled
	Apr 24 06:19:56 pm01 cib[3589]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/crmd/86, version=0.4.20)
	Apr 24 06:19:56 pm01 IPaddr2(prmIp)[5127]: INFO: IP status = ok, IP_CIP=
	Apr 24 06:19:56 pm01 lrmd[3591]:    info: finished - rsc:prmIp action:stop call_id:29 pid:5127 exit-code:0 exec-time:77ms queue-time:0ms
	Apr 24 06:19:56 pm01 crmd[3594]:  notice: Result of stop operation for prmIp on pm01: 0 (ok)
	Apr 24 06:19:56 pm01 cib[3589]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/87)
	Apr 24 06:19:56 pm01 cib[3589]:    info: Diff: --- 0.4.20 2
	Apr 24 06:19:56 pm01 cib[3589]:    info: Diff: +++ 0.4.21 (null)
	Apr 24 06:19:56 pm01 cib[3589]:    info: +  /cib:  @num_updates=21
	Apr 24 06:19:56 pm01 cib[3589]:    info: +  /cib/status/node_state[@id='3232261507']/lrm[@id='3232261507']/lrm_resources/lrm_resource[@id='prmIp']/lrm_rsc_op[@id='prmIp_last_0']:  @operation_key=prmIp_stop_0, @operation=stop, @transition-key=13:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;13:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=29, @last-run=1492982396, @last-rc-change=1492982396, @exec-time=77
	Apr 24 06:19:56 pm01 cib[3589]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/crmd/87, version=0.4.21)
	Apr 24 06:19:56 pm01 crmd[3594]:    info: Action prmIp_stop_0 (13) confirmed on pm01 (rc=0)
	Apr 24 06:19:56 pm01 crmd[3594]:  notice: Initiating stop operation prmFs_stop_0 locally on pm01
	Apr 24 06:19:56 pm01 lrmd[3591]:    info: Cancelling ocf operation prmFs_monitor_10000
	Apr 24 06:19:56 pm01 crmd[3594]:    info: Performing key=10:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8 op=prmFs_stop_0
	Apr 24 06:19:56 pm01 lrmd[3591]:    info: executing - rsc:prmFs action:stop call_id:31
	Apr 24 06:19:56 pm01 crmd[3594]:    info: Result of monitor operation for prmFs on pm01: Cancelled
	Apr 24 06:19:56 pm01 Filesystem(prmFs)[5180]: INFO: Running stop for /dev/vdb2 on /dbfp
	Apr 24 06:19:56 pm01 Filesystem(prmFs)[5180]: INFO: Trying to unmount /dbfp
	Apr 24 06:19:56 pm01 Filesystem(prmFs)[5180]: INFO: unmounted /dbfp successfully
	Apr 24 06:19:56 pm01 lrmd[3591]:    info: finished - rsc:prmFs action:stop call_id:31 pid:5180 exit-code:0 exec-time:136ms queue-time:0ms
	Apr 24 06:19:56 pm01 crmd[3594]:  notice: Result of stop operation for prmFs on pm01: 0 (ok)
	Apr 24 06:19:56 pm01 cib[3589]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/88)
	Apr 24 06:19:56 pm01 cib[3589]:    info: Diff: --- 0.4.21 2
	Apr 24 06:19:56 pm01 cib[3589]:    info: Diff: +++ 0.4.22 (null)
	Apr 24 06:19:56 pm01 cib[3589]:    info: +  /cib:  @num_updates=22
	Apr 24 06:19:56 pm01 cib[3589]:    info: +  /cib/status/node_state[@id='3232261507']/lrm[@id='3232261507']/lrm_resources/lrm_resource[@id='prmFs']/lrm_rsc_op[@id='prmFs_last_0']:  @operation_key=prmFs_stop_0, @operation=stop, @transition-key=10:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;10:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=31, @last-run=1492982396, @last-rc-change=1492982396, @exec-time=136
	Apr 24 06:19:56 pm01 crmd[3594]:    info: Action prmFs_stop_0 (10) confirmed on pm01 (rc=0)
	Apr 24 06:19:56 pm01 crmd[3594]:  notice: Initiating stop operation prmEx_stop_0 locally on pm01
	Apr 24 06:19:56 pm01 lrmd[3591]:    info: Cancelling ocf operation prmEx_monitor_10000
	Apr 24 06:19:56 pm01 crmd[3594]:    info: Performing key=7:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8 op=prmEx_stop_0
	Apr 24 06:19:56 pm01 lrmd[3591]:    info: executing - rsc:prmEx action:stop call_id:33
	Apr 24 06:19:56 pm01 cib[3589]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/crmd/88, version=0.4.22)
	Apr 24 06:19:56 pm01 crmd[3594]:    info: Result of monitor operation for prmEx on pm01: Cancelled
	Apr 24 06:19:56 pm01 sfex(prmEx)[5259]: INFO: sfex_daemon: stopping...
	Apr 24 06:19:56 pm01 sfex_daemon: [3905]: info: quit_handler called. now releasing lock
	Apr 24 06:19:56 pm01 sfex_daemon: [3905]: info: lock released
	Apr 24 06:19:56 pm01 sfex_daemon: [3905]: info: Shutdown sfex_daemon with EXIT_SUCCESS
	Apr 24 06:19:56 pm01 sfex(prmEx)[5259]: INFO: sfex_daemon: stopped.
	Apr 24 06:19:56 pm01 lrmd[3591]:    info: finished - rsc:prmEx action:stop call_id:33 pid:5259 exit-code:0 exec-time:113ms queue-time:0ms
	Apr 24 06:19:56 pm01 crmd[3594]:  notice: Result of stop operation for prmEx on pm01: 0 (ok)
	Apr 24 06:19:56 pm01 cib[3589]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/89)
	Apr 24 06:19:56 pm01 cib[3589]:    info: Diff: --- 0.4.22 2
	Apr 24 06:19:56 pm01 cib[3589]:    info: Diff: +++ 0.4.23 (null)
	Apr 24 06:19:56 pm01 cib[3589]:    info: +  /cib:  @num_updates=23
	Apr 24 06:19:56 pm01 cib[3589]:    info: +  /cib/status/node_state[@id='3232261507']/lrm[@id='3232261507']/lrm_resources/lrm_resource[@id='prmEx']/lrm_rsc_op[@id='prmEx_last_0']:  @operation_key=prmEx_stop_0, @operation=stop, @transition-key=7:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;7:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=33, @last-run=1492982396, @last-rc-change=1492982396, @exec-time=113
	Apr 24 06:19:56 pm01 cib[3589]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/crmd/89, version=0.4.23)
	Apr 24 06:19:56 pm01 crmd[3594]:    info: Action prmEx_stop_0 (7) confirmed on pm01 (rc=0)
	Apr 24 06:19:56 pm01 crmd[3594]:  notice: Initiating start operation prmEx_start_0 on pm02
	Apr 24 06:19:57 pm01 cib[3589]:    info: Diff: --- 0.4.23 2
	Apr 24 06:19:57 pm01 cib[3589]:    info: Diff: +++ 0.4.24 (null)
	Apr 24 06:19:57 pm01 cib[3589]:    info: +  /cib:  @num_updates=24
	Apr 24 06:19:57 pm01 cib[3589]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmEx']/lrm_rsc_op[@id='prmEx_last_0']:  @operation_key=prmEx_start_0, @operation=start, @transition-key=8:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;8:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=18, @rc-code=0, @last-run=1492982395, @last-rc-change=1492982395, @exec-time=1107
	Apr 24 06:19:57 pm01 cib[3589]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/16, version=0.4.24)
	Apr 24 06:19:57 pm01 crmd[3594]:    info: Action prmEx_start_0 (8) confirmed on pm02 (rc=0)
	Apr 24 06:19:57 pm01 crmd[3594]:  notice: Initiating monitor operation prmEx_monitor_10000 on pm02
	Apr 24 06:19:57 pm01 crmd[3594]:  notice: Initiating start operation prmFs_start_0 on pm02
	Apr 24 06:19:57 pm01 cib[3589]:    info: Diff: --- 0.4.24 2
	Apr 24 06:19:57 pm01 cib[3589]:    info: Diff: +++ 0.4.25 (null)
	Apr 24 06:19:57 pm01 cib[3589]:    info: +  /cib:  @num_updates=25
	Apr 24 06:19:57 pm01 cib[3589]:    info: ++ /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmEx']:  <lrm_rsc_op id="prmEx_monitor_10000" operation_key="prmEx_monitor_10000" operation="monitor" crm-debug-origin="do_update_resource" crm_feature_set="3.0.11" transition-key="9:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" transition-magic="0:0;9:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" on_node="pm02" call-id="19" rc-code="0" op-status="0" interval="10000" last-rc-change="1492982396" exec-time="4
	Apr 24 06:19:57 pm01 cib[3589]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/17, version=0.4.25)
	Apr 24 06:19:57 pm01 crmd[3594]:    info: Action prmEx_monitor_10000 (9) confirmed on pm02 (rc=0)
	Apr 24 06:19:57 pm01 cib[3589]:    info: Diff: --- 0.4.25 2
	Apr 24 06:19:57 pm01 cib[3589]:    info: Diff: +++ 0.4.26 (null)
	Apr 24 06:19:57 pm01 cib[3589]:    info: +  /cib:  @num_updates=26
	Apr 24 06:19:57 pm01 cib[3589]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmFs']/lrm_rsc_op[@id='prmFs_last_0']:  @operation_key=prmFs_start_0, @operation=start, @transition-key=11:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;11:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=20, @rc-code=0, @last-run=1492982396, @last-rc-change=1492982396, @exec-time=192, @queue-time=0
	Apr 24 06:19:57 pm01 cib[3589]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/18, version=0.4.26)
	Apr 24 06:19:57 pm01 crmd[3594]:    info: Action prmFs_start_0 (11) confirmed on pm02 (rc=0)
	Apr 24 06:19:57 pm01 crmd[3594]:  notice: Initiating monitor operation prmFs_monitor_10000 on pm02
	Apr 24 06:19:57 pm01 crmd[3594]:  notice: Initiating start operation prmIp_start_0 on pm02
	Apr 24 06:19:57 pm01 cib[3589]:    info: Diff: --- 0.4.26 2
	Apr 24 06:19:57 pm01 cib[3589]:    info: Diff: +++ 0.4.27 (null)
	Apr 24 06:19:57 pm01 cib[3589]:    info: +  /cib:  @num_updates=27
	Apr 24 06:19:57 pm01 cib[3589]:    info: ++ /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmFs']:  <lrm_rsc_op id="prmFs_monitor_10000" operation_key="prmFs_monitor_10000" operation="monitor" crm-debug-origin="do_update_resource" crm_feature_set="3.0.11" transition-key="12:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" transition-magic="0:0;12:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" on_node="pm02" call-id="21" rc-code="0" op-status="0" interval="10000" last-rc-change="1492982397" exec-time=
	Apr 24 06:19:57 pm01 cib[3589]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/19, version=0.4.27)
	Apr 24 06:19:57 pm01 crmd[3594]:    info: Action prmFs_monitor_10000 (12) confirmed on pm02 (rc=0)
	Apr 24 06:19:57 pm01 cib[3589]:    info: Diff: --- 0.4.27 2
	Apr 24 06:19:57 pm01 cib[3589]:    info: Diff: +++ 0.4.28 (null)
	Apr 24 06:19:57 pm01 cib[3589]:    info: +  /cib:  @num_updates=28
	Apr 24 06:19:57 pm01 cib[3589]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmIp']/lrm_rsc_op[@id='prmIp_last_0']:  @operation_key=prmIp_start_0, @operation=start, @transition-key=14:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;14:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=22, @rc-code=0, @last-run=1492982397, @last-rc-change=1492982397, @exec-time=173, @queue-time=0
	Apr 24 06:19:57 pm01 cib[3589]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/20, version=0.4.28)
	Apr 24 06:19:57 pm01 crmd[3594]:    info: Action prmIp_start_0 (14) confirmed on pm02 (rc=0)
	Apr 24 06:19:57 pm01 crmd[3594]:  notice: Initiating monitor operation prmIp_monitor_10000 on pm02
	Apr 24 06:19:57 pm01 crmd[3594]:  notice: Initiating start operation prmPg_start_0 on pm02
	Apr 24 06:19:58 pm01 cib[3589]:    info: Diff: --- 0.4.28 2
	Apr 24 06:19:58 pm01 cib[3589]:    info: Diff: +++ 0.4.29 (null)
	Apr 24 06:19:58 pm01 cib[3589]:    info: +  /cib:  @num_updates=29
	Apr 24 06:19:58 pm01 cib[3589]:    info: ++ /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmIp']:  <lrm_rsc_op id="prmIp_monitor_10000" operation_key="prmIp_monitor_10000" operation="monitor" crm-debug-origin="do_update_resource" crm_feature_set="3.0.11" transition-key="15:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" transition-magic="0:0;15:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" on_node="pm02" call-id="23" rc-code="0" op-status="0" interval="10000" last-rc-change="1492982397" exec-time=
	Apr 24 06:19:58 pm01 cib[3589]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/21, version=0.4.29)
	Apr 24 06:19:58 pm01 crmd[3594]:    info: Action prmIp_monitor_10000 (15) confirmed on pm02 (rc=0)
	Apr 24 06:19:59 pm01 cib[3589]:    info: Diff: --- 0.4.29 2
	Apr 24 06:19:59 pm01 cib[3589]:    info: Diff: +++ 0.4.30 (null)
	Apr 24 06:19:59 pm01 cib[3589]:    info: +  /cib:  @num_updates=30
	Apr 24 06:19:59 pm01 cib[3589]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmPg']/lrm_rsc_op[@id='prmPg_last_0']:  @operation_key=prmPg_start_0, @operation=start, @transition-key=16:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;16:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=24, @rc-code=0, @last-run=1492982397, @last-rc-change=1492982397, @exec-time=1419
	Apr 24 06:19:59 pm01 cib[3589]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/22, version=0.4.30)
	Apr 24 06:19:59 pm01 crmd[3594]:    info: Action prmPg_start_0 (16) confirmed on pm02 (rc=0)
	Apr 24 06:19:59 pm01 crmd[3594]:  notice: Initiating monitor operation prmPg_monitor_10000 on pm02
	Apr 24 06:19:59 pm01 cib[3589]:    info: Diff: --- 0.4.30 2
	Apr 24 06:19:59 pm01 cib[3589]:    info: Diff: +++ 0.4.31 (null)
	Apr 24 06:19:59 pm01 cib[3589]:    info: +  /cib:  @num_updates=31
	Apr 24 06:19:59 pm01 cib[3589]:    info: ++ /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmPg']:  <lrm_rsc_op id="prmPg_monitor_10000" operation_key="prmPg_monitor_10000" operation="monitor" crm-debug-origin="do_update_resource" crm_feature_set="3.0.11" transition-key="17:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" transition-magic="0:0;17:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" on_node="pm02" call-id="25" rc-code="0" op-status="0" interval="10000" last-rc-change="1492982398" exec-time=
	Apr 24 06:19:59 pm01 crmd[3594]:    info: Action prmPg_monitor_10000 (17) confirmed on pm02 (rc=0)
	Apr 24 06:19:59 pm01 crmd[3594]:  notice: Transition 5 (Complete=17, Pending=0, Fired=0, Skipped=0, Incomplete=0, Source=/var/lib/pacemaker/pengine/pe-input-5.bz2): Complete
	Apr 24 06:19:59 pm01 crmd[3594]:    info: Input I_TE_SUCCESS received in state S_TRANSITION_ENGINE from notify_crmd
	Apr 24 06:19:59 pm01 crmd[3594]:  notice: State transition S_TRANSITION_ENGINE -> S_IDLE
	Apr 24 06:19:59 pm01 cib[3589]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/23, version=0.4.31)
	Apr 24 06:20:04 pm01 cib[3589]:    info: Reporting our current digest to pm01: d48162483802ecbf1220a69495defa4d for 0.4.31 (0x7f387545af40 0)
```
### 変換の例 (1) ： ノードpm02の ha-log
```
	Apr 24 06:19:55 pm02 cib[13893]:    info: Diff: --- 0.4.16 2
	Apr 24 06:19:55 pm02 attrd[13896]:    info: Setting fail-count-prmPg[pm01]: (null) -> 1 from pm01
	Apr 24 06:19:55 pm02 attrd[13896]:    info: Setting last-failure-prmPg[pm01]: (null) -> 1492982395 from pm01
	Apr 24 06:19:55 pm02 cib[13893]:    info: Diff: +++ 0.4.17 (null)
	Apr 24 06:19:55 pm02 cib[13893]:    info: +  /cib:  @num_updates=17
	Apr 24 06:19:55 pm02 cib[13893]:    info: ++ /cib/status/node_state[@id='3232261507']/lrm[@id='3232261507']/lrm_resources/lrm_resource[@id='prmPg']:  <lrm_rsc_op id="prmPg_last_failure_0" operation_key="prmPg_monitor_10000" operation="monitor" crm-debug-origin="do_update_resource" crm_feature_set="3.0.11" transition-key="17:3:0:0d469cae-6312-4501-a835-dd2771dcd3f8" transition-magic="0:7;17:3:0:0d469cae-6312-4501-a835-dd2771dcd3f8" on_node="pm01" call-id="25" rc-code="7" op-status="0" interval="10000" last-rc-change="1492982395" exec-time
	Apr 24 06:19:55 pm02 cib[13893]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/crmd/82, version=0.4.17)
	Apr 24 06:19:55 pm02 cib[13893]:    info: Diff: --- 0.4.17 2
	Apr 24 06:19:55 pm02 cib[13893]:    info: Diff: +++ 0.4.18 (null)
	Apr 24 06:19:55 pm02 cib[13893]:    info: +  /cib:  @num_updates=18
	Apr 24 06:19:55 pm02 cib[13893]:    info: ++ /cib/status/node_state[@id='3232261507']/transient_attributes[@id='3232261507']/instance_attributes[@id='status-3232261507']:  <nvpair id="status-3232261507-fail-count-prmPg" name="fail-count-prmPg" value="1"/>
	Apr 24 06:19:55 pm02 cib[13893]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/attrd/10, version=0.4.18)
	Apr 24 06:19:55 pm02 cib[13893]:    info: Diff: --- 0.4.18 2
	Apr 24 06:19:55 pm02 cib[13893]:    info: Diff: +++ 0.4.19 (null)
	Apr 24 06:19:55 pm02 cib[13893]:    info: +  /cib:  @num_updates=19
	Apr 24 06:19:55 pm02 cib[13893]:    info: ++ /cib/status/node_state[@id='3232261507']/transient_attributes[@id='3232261507']/instance_attributes[@id='status-3232261507']:  <nvpair id="status-3232261507-last-failure-prmPg" name="last-failure-prmPg" value="1492982395"/>
	Apr 24 06:19:55 pm02 cib[13893]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/attrd/11, version=0.4.19)
	Apr 24 06:19:55 pm02 cib[13893]:    info: Diff: --- 0.4.19 2
	Apr 24 06:19:55 pm02 cib[13893]:    info: Diff: +++ 0.4.20 (null)
	Apr 24 06:19:55 pm02 cib[13893]:    info: +  /cib:  @num_updates=20
	Apr 24 06:19:55 pm02 cib[13893]:    info: +  /cib/status/node_state[@id='3232261507']/lrm[@id='3232261507']/lrm_resources/lrm_resource[@id='prmPg']/lrm_rsc_op[@id='prmPg_last_0']:  @operation_key=prmPg_stop_0, @operation=stop, @transition-key=5:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;5:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=27, @last-run=1492982395, @last-rc-change=1492982395, @exec-time=124
	Apr 24 06:19:55 pm02 cib[13893]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/crmd/86, version=0.4.20)
	Apr 24 06:19:55 pm02 cib[13893]:    info: Diff: --- 0.4.20 2
	Apr 24 06:19:55 pm02 cib[13893]:    info: Diff: +++ 0.4.21 (null)
	Apr 24 06:19:55 pm02 cib[13893]:    info: +  /cib:  @num_updates=21
	Apr 24 06:19:55 pm02 cib[13893]:    info: +  /cib/status/node_state[@id='3232261507']/lrm[@id='3232261507']/lrm_resources/lrm_resource[@id='prmIp']/lrm_rsc_op[@id='prmIp_last_0']:  @operation_key=prmIp_stop_0, @operation=stop, @transition-key=13:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;13:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=29, @last-run=1492982396, @last-rc-change=1492982396, @exec-time=77
	Apr 24 06:19:55 pm02 cib[13893]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/crmd/87, version=0.4.21)
	Apr 24 06:19:55 pm02 cib[13893]:    info: Diff: --- 0.4.21 2
	Apr 24 06:19:55 pm02 cib[13893]:    info: Diff: +++ 0.4.22 (null)
	Apr 24 06:19:55 pm02 cib[13893]:    info: +  /cib:  @num_updates=22
	Apr 24 06:19:55 pm02 cib[13893]:    info: +  /cib/status/node_state[@id='3232261507']/lrm[@id='3232261507']/lrm_resources/lrm_resource[@id='prmFs']/lrm_rsc_op[@id='prmFs_last_0']:  @operation_key=prmFs_stop_0, @operation=stop, @transition-key=10:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;10:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=31, @last-run=1492982396, @last-rc-change=1492982396, @exec-time=136
	Apr 24 06:19:55 pm02 cib[13893]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/crmd/88, version=0.4.22)
	Apr 24 06:19:55 pm02 cib[13893]:    info: Diff: --- 0.4.22 2
	Apr 24 06:19:55 pm02 cib[13893]:    info: Diff: +++ 0.4.23 (null)
	Apr 24 06:19:55 pm02 cib[13893]:    info: +  /cib:  @num_updates=23
	Apr 24 06:19:55 pm02 cib[13893]:    info: +  /cib/status/node_state[@id='3232261507']/lrm[@id='3232261507']/lrm_resources/lrm_resource[@id='prmEx']/lrm_rsc_op[@id='prmEx_last_0']:  @operation_key=prmEx_stop_0, @operation=stop, @transition-key=7:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;7:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=33, @last-run=1492982396, @last-rc-change=1492982396, @exec-time=113
	Apr 24 06:19:55 pm02 cib[13893]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/crmd/89, version=0.4.23)
⑥	Apr 24 06:19:55 pm02 crmd[13898]:    info: Performing key=8:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8 op=prmEx_start_0
	Apr 24 06:19:55 pm02 lrmd[13895]:    info: executing - rsc:prmEx action:start call_id:18
	Apr 24 06:19:55 pm02 sfex(prmEx)[14140]: INFO: sfex_daemon: starting...
	Apr 24 06:19:55 pm02 sfex_daemon: [14150]: info: Starting SFeX Daemon...
	Apr 24 06:19:56 pm02 sfex_daemon: [14150]: info: lock acquired
	Apr 24 06:19:56 pm02 sfex_daemon: [14151]: info: SFeX Daemon started.
	Apr 24 06:19:56 pm02 sfex(prmEx)[14140]: INFO: sfex_daemon: started.
	Apr 24 06:19:56 pm02 lrmd[13895]:    info: finished - rsc:prmEx action:start call_id:18 pid:14140 exit-code:0 exec-time:1107ms queue-time:0ms
	Apr 24 06:19:56 pm02 crmd[13898]:    info: Managed sfex_meta-data_0 process 14159 exited with rc=0
⑦	Apr 24 06:19:56 pm02 crmd[13898]:  notice: Result of start operation for prmEx on pm02: 0 (ok)
	Apr 24 06:19:56 pm02 cib[13893]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/16)
	Apr 24 06:19:56 pm02 cib[13893]:    info: Diff: --- 0.4.23 2
	Apr 24 06:19:56 pm02 cib[13893]:    info: Diff: +++ 0.4.24 (null)
	Apr 24 06:19:56 pm02 cib[13893]:    info: +  /cib:  @num_updates=24
	Apr 24 06:19:56 pm02 cib[13893]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmEx']/lrm_rsc_op[@id='prmEx_last_0']:  @operation_key=prmEx_start_0, @operation=start, @transition-key=8:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;8:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=18, @rc-code=0, @last-run=1492982395, @last-rc-change=1492982395, @exec-time=1107
	Apr 24 06:19:56 pm02 cib[13893]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/16, version=0.4.24)
	Apr 24 06:19:56 pm02 crmd[13898]:    info: Performing key=9:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8 op=prmEx_monitor_10000
	Apr 24 06:19:56 pm02 crmd[13898]:    info: Performing key=11:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8 op=prmFs_start_0
	Apr 24 06:19:56 pm02 lrmd[13895]:    info: executing - rsc:prmFs action:start call_id:20
	Apr 24 06:19:56 pm02 crmd[13898]:    info: Result of monitor operation for prmEx on pm02: 0 (ok)
	Apr 24 06:19:56 pm02 cib[13893]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/17)
	Apr 24 06:19:56 pm02 cib[13893]:    info: Diff: --- 0.4.24 2
	Apr 24 06:19:56 pm02 cib[13893]:    info: Diff: +++ 0.4.25 (null)
	Apr 24 06:19:56 pm02 cib[13893]:    info: +  /cib:  @num_updates=25
	Apr 24 06:19:56 pm02 cib[13893]:    info: ++ /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmEx']:  <lrm_rsc_op id="prmEx_monitor_10000" operation_key="prmEx_monitor_10000" operation="monitor" crm-debug-origin="do_update_resource" crm_feature_set="3.0.11" transition-key="9:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" transition-magic="0:0;9:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" on_node="pm02" call-id="19" rc-code="0" op-status="0" interval="10000" last-rc-change="1492982396" exec-time="4
	Apr 24 06:19:56 pm02 cib[13893]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/17, version=0.4.25)
	Apr 24 06:19:57 pm02 Filesystem(prmFs)[14164]: INFO: Running start for /dev/vdb2 on /dbfp
	Apr 24 06:19:57 pm02 Filesystem(prmFs)[14164]: INFO: Starting filesystem check on /dev/vdb2
	Apr 24 06:19:57 pm02 lrmd[13895]:    info: finished - rsc:prmFs action:start call_id:20 pid:14164 exit-code:0 exec-time:192ms queue-time:0ms
	Apr 24 06:19:57 pm02 crmd[13898]:    info: Managed Filesystem_meta-data_0 process 14239 exited with rc=0
	Apr 24 06:19:57 pm02 crmd[13898]:  notice: Result of start operation for prmFs on pm02: 0 (ok)
	Apr 24 06:19:57 pm02 cib[13893]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/18)
	Apr 24 06:19:57 pm02 cib[13893]:    info: Diff: --- 0.4.25 2
	Apr 24 06:19:57 pm02 cib[13893]:    info: Diff: +++ 0.4.26 (null)
	Apr 24 06:19:57 pm02 cib[13893]:    info: +  /cib:  @num_updates=26
	Apr 24 06:19:57 pm02 cib[13893]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmFs']/lrm_rsc_op[@id='prmFs_last_0']:  @operation_key=prmFs_start_0, @operation=start, @transition-key=11:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;11:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=20, @rc-code=0, @last-run=1492982396, @last-rc-change=1492982396, @exec-time=192, @queue-time=0
	Apr 24 06:19:57 pm02 cib[13893]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/18, version=0.4.26)
	Apr 24 06:19:57 pm02 crmd[13898]:    info: Performing key=12:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8 op=prmFs_monitor_10000
	Apr 24 06:19:57 pm02 crmd[13898]:    info: Performing key=14:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8 op=prmIp_start_0
	Apr 24 06:19:57 pm02 lrmd[13895]:    info: executing - rsc:prmIp action:start call_id:22
	Apr 24 06:19:57 pm02 crmd[13898]:    info: Result of monitor operation for prmFs on pm02: 0 (ok)
	Apr 24 06:19:57 pm02 cib[13893]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/19)
	Apr 24 06:19:57 pm02 cib[13893]:    info: Diff: --- 0.4.26 2
	Apr 24 06:19:57 pm02 cib[13893]:    info: Diff: +++ 0.4.27 (null)
	Apr 24 06:19:57 pm02 cib[13893]:    info: +  /cib:  @num_updates=27
	Apr 24 06:19:57 pm02 cib[13893]:    info: ++ /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmFs']:  <lrm_rsc_op id="prmFs_monitor_10000" operation_key="prmFs_monitor_10000" operation="monitor" crm-debug-origin="do_update_resource" crm_feature_set="3.0.11" transition-key="12:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" transition-magic="0:0;12:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" on_node="pm02" call-id="21" rc-code="0" op-status="0" interval="10000" last-rc-change="1492982397" exec-time=
	Apr 24 06:19:57 pm02 cib[13893]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/19, version=0.4.27)
	Apr 24 06:19:57 pm02 IPaddr2(prmIp)[14246]: INFO: Adding inet address 192.168.201.100/24 with broadcast address 192.168.201.255 to device eth1
	Apr 24 06:19:57 pm02 IPaddr2(prmIp)[14246]: INFO: Bringing device eth1 up
	Apr 24 06:19:57 pm02 IPaddr2(prmIp)[14246]: INFO: /usr/lib64/heartbeat/send_arp -i 200 -r 5 -p /var/run/resource-agents/send_arp-192.168.201.100 eth1 192.168.201.100 auto not_used not_used
	Apr 24 06:19:57 pm02 lrmd[13895]:    info: finished - rsc:prmIp action:start call_id:22 pid:14246 exit-code:0 exec-time:173ms queue-time:0ms
	Apr 24 06:19:57 pm02 crmd[13898]:    info: Managed IPaddr2_meta-data_0 process 14361 exited with rc=0
	Apr 24 06:19:57 pm02 crmd[13898]:  notice: Result of start operation for prmIp on pm02: 0 (ok)
	Apr 24 06:19:57 pm02 cib[13893]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/20)
	Apr 24 06:19:57 pm02 cib[13893]:    info: Diff: --- 0.4.27 2
	Apr 24 06:19:57 pm02 cib[13893]:    info: Diff: +++ 0.4.28 (null)
	Apr 24 06:19:57 pm02 cib[13893]:    info: +  /cib:  @num_updates=28
	Apr 24 06:19:57 pm02 cib[13893]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmIp']/lrm_rsc_op[@id='prmIp_last_0']:  @operation_key=prmIp_start_0, @operation=start, @transition-key=14:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;14:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=22, @rc-code=0, @last-run=1492982397, @last-rc-change=1492982397, @exec-time=173, @queue-time=0
	Apr 24 06:19:57 pm02 cib[13893]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/20, version=0.4.28)
	Apr 24 06:19:57 pm02 crmd[13898]:    info: Performing key=15:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8 op=prmIp_monitor_10000
	Apr 24 06:19:57 pm02 crmd[13898]:    info: Performing key=16:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8 op=prmPg_start_0
	Apr 24 06:19:57 pm02 lrmd[13895]:    info: executing - rsc:prmPg action:start call_id:24
	Apr 24 06:19:57 pm02 crmd[13898]:    info: Result of monitor operation for prmIp on pm02: 0 (ok)
	Apr 24 06:19:57 pm02 cib[13893]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/21)
	Apr 24 06:19:57 pm02 cib[13893]:    info: Diff: --- 0.4.28 2
	Apr 24 06:19:57 pm02 cib[13893]:    info: Diff: +++ 0.4.29 (null)
	Apr 24 06:19:57 pm02 cib[13893]:    info: +  /cib:  @num_updates=29
	Apr 24 06:19:57 pm02 cib[13893]:    info: ++ /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmIp']:  <lrm_rsc_op id="prmIp_monitor_10000" operation_key="prmIp_monitor_10000" operation="monitor" crm-debug-origin="do_update_resource" crm_feature_set="3.0.11" transition-key="15:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" transition-magic="0:0;15:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" on_node="pm02" call-id="23" rc-code="0" op-status="0" interval="10000" last-rc-change="1492982397" exec-time=
	Apr 24 06:19:57 pm02 cib[13893]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/21, version=0.4.29)
	Apr 24 06:19:57 pm02 pgsql(prmPg)[14367]: INFO: server starting
	Apr 24 06:19:57 pm02 pgsql(prmPg)[14367]: INFO: PostgreSQL start command sent.
	Apr 24 06:19:57 pm02 pgsql(prmPg)[14367]: WARNING: psql: FATAL: the database system is starting up
	Apr 24 06:19:57 pm02 pgsql(prmPg)[14367]: WARNING: PostgreSQL template1 isn't running. rc=2
	Apr 24 06:19:57 pm02 pgsql(prmPg)[14367]: WARNING: Connection error (connection to the server went bad and the session was not interactive) occurred while executing the psql command.
	Apr 24 06:19:58 pm02 pgsql(prmPg)[14367]: INFO: PostgreSQL is started.
	Apr 24 06:19:58 pm02 lrmd[13895]:    info: finished - rsc:prmPg action:start call_id:24 pid:14367 exit-code:0 exec-time:1419ms queue-time:0ms
	Apr 24 06:19:58 pm02 crmd[13898]:    info: Managed pgsql_meta-data_0 process 14590 exited with rc=0
	Apr 24 06:19:58 pm02 crmd[13898]:  notice: Result of start operation for prmPg on pm02: 0 (ok)
	Apr 24 06:19:58 pm02 cib[13893]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/22)
	Apr 24 06:19:58 pm02 cib[13893]:    info: Diff: --- 0.4.29 2
	Apr 24 06:19:58 pm02 cib[13893]:    info: Diff: +++ 0.4.30 (null)
	Apr 24 06:19:58 pm02 cib[13893]:    info: +  /cib:  @num_updates=30
	Apr 24 06:19:58 pm02 cib[13893]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmPg']/lrm_rsc_op[@id='prmPg_last_0']:  @operation_key=prmPg_start_0, @operation=start, @transition-key=16:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @transition-magic=0:0;16:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8, @call-id=24, @rc-code=0, @last-run=1492982397, @last-rc-change=1492982397, @exec-time=1419
	Apr 24 06:19:58 pm02 cib[13893]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/22, version=0.4.30)
	Apr 24 06:19:58 pm02 crmd[13898]:    info: Performing key=17:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8 op=prmPg_monitor_10000
	Apr 24 06:19:59 pm02 crmd[13898]:    info: Result of monitor operation for prmPg on pm02: 0 (ok)
	Apr 24 06:19:59 pm02 cib[13893]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/23)
	Apr 24 06:19:59 pm02 cib[13893]:    info: Diff: --- 0.4.30 2
	Apr 24 06:19:59 pm02 cib[13893]:    info: Diff: +++ 0.4.31 (null)
	Apr 24 06:19:59 pm02 cib[13893]:    info: +  /cib:  @num_updates=31
	Apr 24 06:19:59 pm02 cib[13893]:    info: ++ /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmPg']:  <lrm_rsc_op id="prmPg_monitor_10000" operation_key="prmPg_monitor_10000" operation="monitor" crm-debug-origin="do_update_resource" crm_feature_set="3.0.11" transition-key="17:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" transition-magic="0:0;17:5:0:0d469cae-6312-4501-a835-dd2771dcd3f8" on_node="pm02" call-id="25" rc-code="0" op-status="0" interval="10000" last-rc-change="1492982398" exec-time=
	Apr 24 06:19:59 pm02 cib[13893]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/23, version=0.4.31)
	Apr 24 06:20:04 pm02 cib[13893]:    info: Reporting our current digest to pm01: d48162483802ecbf1220a69495defa4d for 0.4.31 (0x7ff3f95d5010 0)
```

## 変換の例 (2)
### 変換の例 (2) ： ノードpm01の ha-log
```
⑩	Apr 24 06:26:35 pm01 ping(prmPing)[10511]: WARNING: 192.168.201.254 is inactive: PING 192.168.201.254 (192.168.201.254) 56(84) bytes of data.#012#012--- 192.168.201.254 ping statistics ---#0122 packets transmitted, 0 received, 100% packet loss, time 999ms
⑪	Apr 24 06:26:35 pm01 attrd[5559]:    info: Setting default_ping_set[pm01]: 100 -> 0 from pm01
	Apr 24 06:26:40 pm01 cib[5556]:    info: Diff: --- 0.6.18 2
	Apr 24 06:26:40 pm01 cib[5556]:    info: Diff: +++ 0.6.19 (null)
	Apr 24 06:26:40 pm01 cib[5556]:    info: +  /cib:  @num_updates=19
	Apr 24 06:26:40 pm01 cib[5556]:    info: +  /cib/status/node_state[@id='3232261507']/transient_attributes[@id='3232261507']/instance_attributes[@id='status-3232261507']/nvpair[@id='status-3232261507-default_ping_set']:  @value=0
	Apr 24 06:26:40 pm01 cib[5556]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/attrd/20, version=0.6.19)
	Apr 24 06:26:40 pm01 lrmd[5558]:    info: Cancelling ocf operation prmPg_monitor_10000
	Apr 24 06:26:40 pm01 crmd[5561]:    info: Performing key=23:15:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf op=prmPg_stop_0
	Apr 24 06:26:40 pm01 lrmd[5558]:    info: executing - rsc:prmPg action:stop call_id:83
	Apr 24 06:26:40 pm01 crmd[5561]:    info: Result of monitor operation for prmPg on pm01: Cancelled
	Apr 24 06:26:43 pm01 lrmd[5558]:    info: finished - rsc:prmPg action:stop call_id:83 pid:10718 exit-code:1 exec-time:3129ms queue-time:0ms
	Apr 24 06:26:43 pm01 crmd[5561]:  notice: Result of stop operation for prmPg on pm01: 1 (unknown error)
	Apr 24 06:26:43 pm01 cib[5556]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/52)
	Apr 24 06:26:43 pm01 cib[5556]:    info: Diff: --- 0.6.19 2
	Apr 24 06:26:43 pm01 cib[5556]:    info: Diff: +++ 0.6.20 (null)
	Apr 24 06:26:43 pm01 cib[5556]:    info: +  /cib:  @num_updates=20
	Apr 24 06:26:43 pm01 cib[5556]:    info: +  /cib/status/node_state[@id='3232261507']/lrm[@id='3232261507']/lrm_resources/lrm_resource[@id='prmPg']/lrm_rsc_op[@id='prmPg_last_0']:  @operation_key=prmPg_stop_0, @operation=stop, @transition-key=23:15:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @transition-magic=0:1;23:15:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @call-id=83, @rc-code=1, @last-run=1492982800, @last-rc-change=1492982800, @exec-time=3129, @queue-time=0
	Apr 24 06:26:43 pm01 cib[5556]:    info: ++ /cib/status/node_state[@id='3232261507']/lrm[@id='3232261507']/lrm_resources/lrm_resource[@id='prmPg']:  <lrm_rsc_op id="prmPg_last_failure_0" operation_key="prmPg_stop_0" operation="stop" crm-debug-origin="do_update_resource" crm_feature_set="3.0.11" transition-key="23:15:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf" transition-magic="0:1;23:15:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf" on_node="pm01" call-id="83" rc-code="1" op-status="0" interval="0" last-run="1492982800" last-rc-change="1492982800"
	Apr 24 06:26:43 pm01 cib[5556]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/crmd/52, version=0.6.20)
	Apr 24 06:26:43 pm01 attrd[5559]:    info: Setting fail-count-prmPg[pm01]: (null) -> INFINITY from pm02
	Apr 24 06:26:43 pm01 attrd[5559]:    info: Setting last-failure-prmPg[pm01]: (null) -> 1492982803 from pm02
	Apr 24 06:26:43 pm01 cib[5556]:    info: Diff: --- 0.6.20 2
	Apr 24 06:26:43 pm01 cib[5556]:    info: Diff: +++ 0.6.21 (null)
	Apr 24 06:26:43 pm01 cib[5556]:    info: +  /cib:  @num_updates=21
	Apr 24 06:26:43 pm01 cib[5556]:    info: ++ /cib/status/node_state[@id='3232261507']/transient_attributes[@id='3232261507']/instance_attributes[@id='status-3232261507']:  <nvpair id="status-3232261507-fail-count-prmPg" name="fail-count-prmPg" value="INFINITY"/>
	Apr 24 06:26:43 pm01 cib[5556]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/attrd/21, version=0.6.21)
	Apr 24 06:26:43 pm01 cib[5556]:    info: Diff: --- 0.6.21 2
	Apr 24 06:26:43 pm01 cib[5556]:    info: Diff: +++ 0.6.22 (null)
	Apr 24 06:26:43 pm01 cib[5556]:    info: +  /cib:  @num_updates=22
	Apr 24 06:26:43 pm01 cib[5556]:    info: ++ /cib/status/node_state[@id='3232261507']/transient_attributes[@id='3232261507']/instance_attributes[@id='status-3232261507']:  <nvpair id="status-3232261507-last-failure-prmPg" name="last-failure-prmPg" value="1492982803"/>
	Apr 24 06:26:43 pm01 cib[5556]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/attrd/22, version=0.6.22)
```
### 変換の例 (2) ： ノードpm02の ha-log
```
⑪	Apr 24 06:26:34 pm02 attrd[16430]:    info: Setting default_ping_set[pm01]: 100 -> 0 from pm01
	Apr 24 06:26:39 pm02 attrd[16430]:    info: Sent update 20 with 2 changes for default_ping_set, id=<n/a>, set=(null)
	Apr 24 06:26:39 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/attrd/20)
	Apr 24 06:26:39 pm02 cib[16427]:    info: Diff: --- 0.6.18 2
	Apr 24 06:26:39 pm02 cib[16427]:    info: Diff: +++ 0.6.19 (null)
	Apr 24 06:26:39 pm02 cib[16427]:    info: +  /cib:  @num_updates=19
	Apr 24 06:26:39 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261507']/transient_attributes[@id='3232261507']/instance_attributes[@id='status-3232261507']/nvpair[@id='status-3232261507-default_ping_set']:  @value=0
	Apr 24 06:26:39 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/attrd/20, version=0.6.19)
	Apr 24 06:26:39 pm02 crmd[16432]:    info: Transition aborted by status-3232261507-default_ping_set doing modify default_ping_set=0: Transient attribute change
	Apr 24 06:26:39 pm02 crmd[16432]:  notice: State transition S_IDLE -> S_POLICY_ENGINE
	Apr 24 06:26:39 pm02 attrd[16430]:    info: Update 20 for default_ping_set: OK (0)
	Apr 24 06:26:39 pm02 attrd[16430]:    info: Update 20 for default_ping_set[pm01]=0: OK (0)
	Apr 24 06:26:39 pm02 attrd[16430]:    info: Update 20 for default_ping_set[pm02]=100: OK (0)
	Apr 24 06:26:40 pm02 pengine[16431]:  notice: On loss of CCM Quorum: Ignore
	Apr 24 06:26:40 pm02 pengine[16431]:    info: Node pm02 is active
	Apr 24 06:26:40 pm02 pengine[16431]:    info: Node pm02 is online
	Apr 24 06:26:40 pm02 pengine[16431]:    info: Node pm01 is active
	Apr 24 06:26:40 pm02 pengine[16431]:    info: Node pm01 is online
	Apr 24 06:26:40 pm02 pengine[16431]:    info:  Resource Group: grpPg
	Apr 24 06:26:40 pm02 pengine[16431]:    info:      prmEx#011(ocf::heartbeat:sfex):#011Started pm01
	Apr 24 06:26:40 pm02 pengine[16431]:    info:      prmFs#011(ocf::heartbeat:Filesystem):#011Started pm01
	Apr 24 06:26:40 pm02 pengine[16431]:    info:      prmIp#011(ocf::heartbeat:IPaddr2):#011Started pm01
	Apr 24 06:26:40 pm02 pengine[16431]:    info:      prmPg#011(ocf::heartbeat:pgsql):#011Started pm01
	Apr 24 06:26:40 pm02 pengine[16431]:    info:  Resource Group: grpStonith1
	Apr 24 06:26:40 pm02 pengine[16431]:    info:      prmStonith1-1#011(stonith:external/stonith-helper):#011Started pm02
	Apr 24 06:26:40 pm02 pengine[16431]:    info:      prmStonith1-2#011(stonith:external/libvirt):#011Started pm02
	Apr 24 06:26:40 pm02 pengine[16431]:    info:  Resource Group: grpStonith2
	Apr 24 06:26:40 pm02 pengine[16431]:    info:      prmStonith2-1#011(stonith:external/stonith-helper):#011Started pm01
	Apr 24 06:26:40 pm02 pengine[16431]:    info:      prmStonith2-2#011(stonith:external/libvirt):#011Started pm01
	Apr 24 06:26:40 pm02 pengine[16431]:    info:  Clone Set: clnDiskd1 [prmDiskd1]
	Apr 24 06:26:40 pm02 pengine[16431]:    info:      Started: [ pm01 pm02 ]
	Apr 24 06:26:40 pm02 pengine[16431]:    info:  Clone Set: clnDiskd2 [prmDiskd2]
	Apr 24 06:26:40 pm02 pengine[16431]:    info:      Started: [ pm01 pm02 ]
	Apr 24 06:26:40 pm02 pengine[16431]:    info:  Clone Set: clnPing [prmPing]
	Apr 24 06:26:40 pm02 pengine[16431]:    info:      Started: [ pm01 pm02 ]
	Apr 24 06:26:40 pm02 pengine[16431]:    info:  Start recurring monitor (10s) for prmEx on pm02
	Apr 24 06:26:40 pm02 pengine[16431]:    info:  Start recurring monitor (10s) for prmFs on pm02
	Apr 24 06:26:40 pm02 pengine[16431]:    info:  Start recurring monitor (10s) for prmIp on pm02
	Apr 24 06:26:40 pm02 pengine[16431]:    info:  Start recurring monitor (10s) for prmPg on pm02
	Apr 24 06:26:40 pm02 pengine[16431]:  notice: Move    prmEx#011(Started pm01 -> pm02)
	Apr 24 06:26:40 pm02 pengine[16431]:  notice: Move    prmFs#011(Started pm01 -> pm02)
	Apr 24 06:26:40 pm02 pengine[16431]:  notice: Move    prmIp#011(Started pm01 -> pm02)
	Apr 24 06:26:40 pm02 pengine[16431]:  notice: Move    prmPg#011(Started pm01 -> pm02)
	Apr 24 06:26:40 pm02 pengine[16431]:    info: Leave   prmStonith1-1#011(Started pm02)
	Apr 24 06:26:40 pm02 pengine[16431]:    info: Leave   prmStonith1-2#011(Started pm02)
	Apr 24 06:26:40 pm02 pengine[16431]:    info: Leave   prmStonith2-1#011(Started pm01)
	Apr 24 06:26:40 pm02 pengine[16431]:    info: Leave   prmStonith2-2#011(Started pm01)
	Apr 24 06:26:40 pm02 pengine[16431]:    info: Leave   prmDiskd1:0#011(Started pm02)
	Apr 24 06:26:40 pm02 pengine[16431]:    info: Leave   prmDiskd1:1#011(Started pm01)
	Apr 24 06:26:40 pm02 pengine[16431]:    info: Leave   prmDiskd2:0#011(Started pm02)
	Apr 24 06:26:40 pm02 pengine[16431]:    info: Leave   prmDiskd2:1#011(Started pm01)
	Apr 24 06:26:40 pm02 pengine[16431]:    info: Leave   prmPing:0#011(Started pm02)
	Apr 24 06:26:40 pm02 pengine[16431]:    info: Leave   prmPing:1#011(Started pm01)
	Apr 24 06:26:40 pm02 pengine[16431]:  notice: Calculated transition 15, saving inputs in /var/lib/pacemaker/pengine/pe-input-15.bz2
	Apr 24 06:26:40 pm02 crmd[16432]:    info: State transition S_POLICY_ENGINE -> S_TRANSITION_ENGINE
	Apr 24 06:26:40 pm02 crmd[16432]:    info: Processing graph 15 (ref=pe_calc-dc-1492982799-131) derived from /var/lib/pacemaker/pengine/pe-input-15.bz2
	Apr 24 06:26:40 pm02 crmd[16432]:  notice: Initiating stop operation prmPg_stop_0 on pm01
	Apr 24 06:26:43 pm02 cib[16427]:    info: Diff: --- 0.6.19 2
	Apr 24 06:26:43 pm02 cib[16427]:    info: Diff: +++ 0.6.20 (null)
	Apr 24 06:26:43 pm02 cib[16427]:    info: +  /cib:  @num_updates=20
	Apr 24 06:26:43 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261507']/lrm[@id='3232261507']/lrm_resources/lrm_resource[@id='prmPg']/lrm_rsc_op[@id='prmPg_last_0']:  @operation_key=prmPg_stop_0, @operation=stop, @transition-key=23:15:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @transition-magic=0:1;23:15:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @call-id=83, @rc-code=1, @last-run=1492982800, @last-rc-change=1492982800, @exec-time=3129, @queue-time=0
	Apr 24 06:26:43 pm02 cib[16427]:    info: ++ /cib/status/node_state[@id='3232261507']/lrm[@id='3232261507']/lrm_resources/lrm_resource[@id='prmPg']:  <lrm_rsc_op id="prmPg_last_failure_0" operation_key="prmPg_stop_0" operation="stop" crm-debug-origin="do_update_resource" crm_feature_set="3.0.11" transition-key="23:15:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf" transition-magic="0:1;23:15:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf" on_node="pm01" call-id="83" rc-code="1" op-status="0" interval="0" last-run="1492982800" last-rc-change="1492982800"
	Apr 24 06:26:43 pm02 crmd[16432]: warning: Action 23 (prmPg_stop_0) on pm01 failed (target: 0 vs. rc: 1): Error
	Apr 24 06:26:43 pm02 crmd[16432]:  notice: Transition aborted by operation prmPg_stop_0 'modify' on pm01: Event failed
	Apr 24 06:26:43 pm02 crmd[16432]:    info: Action prmPg_stop_0 (23) confirmed on pm01 (rc=1)
	Apr 24 06:26:43 pm02 crmd[16432]:    info: Updating failcount for prmPg on pm01 after failed stop: rc=1 (update=INFINITY, time=1492982803)
	Apr 24 06:26:43 pm02 crmd[16432]:    info: Detected action (15.23) prmPg_stop_0.83=unknown error: failed
	Apr 24 06:26:43 pm02 crmd[16432]: warning: Action 23 (prmPg_stop_0) on pm01 failed (target: 0 vs. rc: 1): Error
	Apr 24 06:26:43 pm02 crmd[16432]:    info: Transition aborted by operation prmPg_stop_0 'create' on pm01: Event failed
	Apr 24 06:26:43 pm02 crmd[16432]:    info: Action prmPg_stop_0 (23) confirmed on pm01 (rc=1)
	Apr 24 06:26:43 pm02 crmd[16432]:    info: Updating failcount for prmPg on pm01 after failed stop: rc=1 (update=INFINITY, time=1492982803)
	Apr 24 06:26:43 pm02 crmd[16432]:    info: Detected action (15.23) prmPg_stop_0.83=unknown error: failed
	Apr 24 06:26:43 pm02 crmd[16432]:  notice: Transition 15 (Complete=2, Pending=0, Fired=0, Skipped=0, Incomplete=15, Source=/var/lib/pacemaker/pengine/pe-input-15.bz2): Complete
	Apr 24 06:26:43 pm02 crmd[16432]:    info: State transition S_TRANSITION_ENGINE -> S_POLICY_ENGINE
	Apr 24 06:26:43 pm02 attrd[16430]:    info: Setting fail-count-prmPg[pm01]: (null) -> INFINITY from pm02
	Apr 24 06:26:43 pm02 attrd[16430]:    info: Sent update 21 with 1 changes for fail-count-prmPg, id=<n/a>, set=(null)
	Apr 24 06:26:43 pm02 attrd[16430]:    info: Setting last-failure-prmPg[pm01]: (null) -> 1492982803 from pm02
	Apr 24 06:26:43 pm02 attrd[16430]:    info: Sent update 22 with 1 changes for last-failure-prmPg, id=<n/a>, set=(null)
	Apr 24 06:26:43 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm01/crmd/52, version=0.6.20)
	Apr 24 06:26:43 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/attrd/21)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: On loss of CCM Quorum: Ignore
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Node pm02 is active
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Node pm02 is online
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Node pm01 is active
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Node pm01 is online
	Apr 24 06:26:43 pm02 pengine[16431]: warning: Processing failed op stop for prmPg on pm01: unknown error (1)
	Apr 24 06:26:43 pm02 pengine[16431]: warning: Processing failed op stop for prmPg on pm01: unknown error (1)
	Apr 24 06:26:43 pm02 pengine[16431]: warning: Node pm01 will be fenced because of resource failure(s)
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Resource Group: grpPg
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmEx#011(ocf::heartbeat:sfex):#011Started pm01
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmFs#011(ocf::heartbeat:Filesystem):#011Started pm01
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmIp#011(ocf::heartbeat:IPaddr2):#011Started pm01
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmPg#011(ocf::heartbeat:pgsql):#011FAILED pm01
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Resource Group: grpStonith1
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmStonith1-1#011(stonith:external/stonith-helper):#011Started pm02
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmStonith1-2#011(stonith:external/libvirt):#011Started pm02
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Resource Group: grpStonith2
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmStonith2-1#011(stonith:external/stonith-helper):#011Started pm01
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmStonith2-2#011(stonith:external/libvirt):#011Started pm01
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Clone Set: clnDiskd1 [prmDiskd1]
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      Started: [ pm01 pm02 ]
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Clone Set: clnDiskd2 [prmDiskd2]
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      Started: [ pm01 pm02 ]
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Clone Set: clnPing [prmPing]
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      Started: [ pm01 pm02 ]
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Resource prmDiskd1:1 cannot run anywhere
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Resource prmDiskd2:1 cannot run anywhere
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Resource prmPing:1 cannot run anywhere
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmStonith2-1: Rolling back scores from prmStonith2-2
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Resource prmStonith2-1 cannot run anywhere
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Resource prmStonith2-2 cannot run anywhere
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Start recurring monitor (10s) for prmEx on pm02
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Start recurring monitor (10s) for prmFs on pm02
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Start recurring monitor (10s) for prmIp on pm02
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Start recurring monitor (10s) for prmPg on pm02
	Apr 24 06:26:43 pm02 pengine[16431]: warning: Scheduling Node pm01 for STONITH
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmEx_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmFs_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmIp_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Stop of failed resource prmPg is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmStonith2-1_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmStonith2-2_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmDiskd1:1_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmDiskd2:1_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmPing:1_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Move    prmEx#011(Started pm01 -> pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Move    prmFs#011(Started pm01 -> pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Move    prmIp#011(Started pm01 -> pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Recover prmPg#011(Started pm01 -> pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Leave   prmStonith1-1#011(Started pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Leave   prmStonith1-2#011(Started pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Stop    prmStonith2-1#011(pm01)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Stop    prmStonith2-2#011(pm01)
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Leave   prmDiskd1:0#011(Started pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Stop    prmDiskd1:1#011(pm01)
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Leave   prmDiskd2:0#011(Started pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Stop    prmDiskd2:1#011(pm01)
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Leave   prmPing:0#011(Started pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Stop    prmPing:1#011(pm01)
	Apr 24 06:26:43 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/attrd/22)
	Apr 24 06:26:43 pm02 cib[16427]:    info: Diff: --- 0.6.20 2
	Apr 24 06:26:43 pm02 cib[16427]:    info: Diff: +++ 0.6.21 (null)
	Apr 24 06:26:43 pm02 cib[16427]:    info: +  /cib:  @num_updates=21
	Apr 24 06:26:43 pm02 cib[16427]:    info: ++ /cib/status/node_state[@id='3232261507']/transient_attributes[@id='3232261507']/instance_attributes[@id='status-3232261507']:  <nvpair id="status-3232261507-fail-count-prmPg" name="fail-count-prmPg" value="INFINITY"/>
	Apr 24 06:26:43 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/attrd/21, version=0.6.21)
	Apr 24 06:26:43 pm02 attrd[16430]:    info: Update 21 for fail-count-prmPg: OK (0)
	Apr 24 06:26:43 pm02 attrd[16430]:    info: Update 21 for fail-count-prmPg[pm01]=INFINITY: OK (0)
	Apr 24 06:26:43 pm02 cib[16427]:    info: Diff: --- 0.6.21 2
	Apr 24 06:26:43 pm02 cib[16427]:    info: Diff: +++ 0.6.22 (null)
	Apr 24 06:26:43 pm02 cib[16427]:    info: +  /cib:  @num_updates=22
	Apr 24 06:26:43 pm02 cib[16427]:    info: ++ /cib/status/node_state[@id='3232261507']/transient_attributes[@id='3232261507']/instance_attributes[@id='status-3232261507']:  <nvpair id="status-3232261507-last-failure-prmPg" name="last-failure-prmPg" value="1492982803"/>
	Apr 24 06:26:43 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/attrd/22, version=0.6.22)
	Apr 24 06:26:43 pm02 attrd[16430]:    info: Update 22 for last-failure-prmPg: OK (0)
	Apr 24 06:26:43 pm02 attrd[16430]:    info: Update 22 for last-failure-prmPg[pm01]=1492982803: OK (0)
	Apr 24 06:26:43 pm02 pengine[16431]: warning: Calculated transition 16 (with warnings), saving inputs in /var/lib/pacemaker/pengine/pe-warn-0.bz2
	Apr 24 06:26:43 pm02 crmd[16432]:    info: Transition aborted by status-3232261507-fail-count-prmPg doing create fail-count-prmPg=INFINITY: Transient attribute change
	Apr 24 06:26:43 pm02 crmd[16432]:    info: Transition aborted by status-3232261507-last-failure-prmPg doing create last-failure-prmPg=1492982803: Transient attribute change
	Apr 24 06:26:43 pm02 crmd[16432]:    info: pe_calc calculation pe_calc-dc-1492982803-133 is obsolete
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: On loss of CCM Quorum: Ignore
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Node pm02 is active
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Node pm02 is online
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Node pm01 is active
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Node pm01 is online
	Apr 24 06:26:43 pm02 pengine[16431]: warning: Processing failed op stop for prmPg on pm01: unknown error (1)
	Apr 24 06:26:43 pm02 pengine[16431]: warning: Processing failed op stop for prmPg on pm01: unknown error (1)
	Apr 24 06:26:43 pm02 pengine[16431]: warning: Node pm01 will be fenced because of resource failure(s)
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Resource Group: grpPg
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmEx#011(ocf::heartbeat:sfex):#011Started pm01
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmFs#011(ocf::heartbeat:Filesystem):#011Started pm01
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmIp#011(ocf::heartbeat:IPaddr2):#011Started pm01
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmPg#011(ocf::heartbeat:pgsql):#011FAILED pm01
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Resource Group: grpStonith1
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmStonith1-1#011(stonith:external/stonith-helper):#011Started pm02
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmStonith1-2#011(stonith:external/libvirt):#011Started pm02
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Resource Group: grpStonith2
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmStonith2-1#011(stonith:external/stonith-helper):#011Started pm01
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      prmStonith2-2#011(stonith:external/libvirt):#011Started pm01
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Clone Set: clnDiskd1 [prmDiskd1]
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      Started: [ pm01 pm02 ]
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Clone Set: clnDiskd2 [prmDiskd2]
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      Started: [ pm01 pm02 ]
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Clone Set: clnPing [prmPing]
	Apr 24 06:26:43 pm02 pengine[16431]:    info:      Started: [ pm01 pm02 ]
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmPg has failed INFINITY times on pm01
	Apr 24 06:26:43 pm02 pengine[16431]: warning: Forcing prmPg away from pm01 after 1000000 failures (max=1)
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Resource prmDiskd1:1 cannot run anywhere
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Resource prmDiskd2:1 cannot run anywhere
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Resource prmPing:1 cannot run anywhere
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmStonith2-1: Rolling back scores from prmStonith2-2
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Resource prmStonith2-1 cannot run anywhere
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Resource prmStonith2-2 cannot run anywhere
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Start recurring monitor (10s) for prmEx on pm02
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Start recurring monitor (10s) for prmFs on pm02
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Start recurring monitor (10s) for prmIp on pm02
	Apr 24 06:26:43 pm02 pengine[16431]:    info:  Start recurring monitor (10s) for prmPg on pm02
	Apr 24 06:26:43 pm02 pengine[16431]: warning: Scheduling Node pm01 for STONITH
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmEx_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmFs_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmIp_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Stop of failed resource prmPg is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmStonith2-1_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmStonith2-2_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmDiskd1:1_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmDiskd2:1_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:    info: prmPing:1_stop_0 is implicit after pm01 is fenced
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Move    prmEx#011(Started pm01 -> pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Move    prmFs#011(Started pm01 -> pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Move    prmIp#011(Started pm01 -> pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Recover prmPg#011(Started pm01 -> pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Leave   prmStonith1-1#011(Started pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Leave   prmStonith1-2#011(Started pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Stop    prmStonith2-1#011(pm01)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Stop    prmStonith2-2#011(pm01)
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Leave   prmDiskd1:0#011(Started pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Stop    prmDiskd1:1#011(pm01)
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Leave   prmDiskd2:0#011(Started pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Stop    prmDiskd2:1#011(pm01)
	Apr 24 06:26:43 pm02 pengine[16431]:    info: Leave   prmPing:0#011(Started pm02)
	Apr 24 06:26:43 pm02 pengine[16431]:  notice: Stop    prmPing:1#011(pm01)
	Apr 24 06:26:43 pm02 pengine[16431]: warning: Calculated transition 17 (with warnings), saving inputs in /var/lib/pacemaker/pengine/pe-warn-1.bz2
	Apr 24 06:26:43 pm02 crmd[16432]:    info: State transition S_POLICY_ENGINE -> S_TRANSITION_ENGINE
	Apr 24 06:26:43 pm02 crmd[16432]:    info: Processing graph 17 (ref=pe_calc-dc-1492982803-134) derived from /var/lib/pacemaker/pengine/pe-warn-1.bz2
⑫	Apr 24 06:26:43 pm02 crmd[16432]:  notice: Requesting fencing (reboot) of node pm01
	Apr 24 06:26:43 pm02 stonith-ng[16428]:  notice: Client crmd.16432.c4085a23 wants to fence (reboot) 'pm01' with device '(any)'
	Apr 24 06:26:43 pm02 stonith-ng[16428]:  notice: Requesting peer fencing (reboot) of pm01
	Apr 24 06:26:43 pm02 stonith-ng[16428]:    info: Query result 1 of 2 from pm01 for pm01/reboot (0 devices) 4f64bf61-9b88-4934-853b-704424f6d7de
	Apr 24 06:26:43 pm02 stonith-ng[16428]:    info: Refreshing port list for prmStonith1-2
	Apr 24 06:26:43 pm02 stonith-ng[16428]:    info: Refreshing port list for prmStonith1-1
	Apr 24 06:26:43 pm02 stonith-ng[16428]:    info: Query result 2 of 2 from pm02 for pm01/reboot (2 devices) 4f64bf61-9b88-4934-853b-704424f6d7de
	Apr 24 06:26:43 pm02 stonith-ng[16428]:    info: Total timeout set to 100 for peer's fencing of pm01 for crmd.16432
	Apr 24 06:26:43 pm02 stonith-ng[16428]:    info: Requesting that 'pm02' perform op 'pm01 reboot' with 'prmStonith1-1' for crmd.16432 (48s)
	Apr 24 06:26:43 pm02 external/stonith-helper[19930]: info: 192.168.201.131 responded.
	Apr 24 06:26:43 pm02 external/stonith-helper[19931]: info: 192.168.101.131 responded.
	Apr 24 06:26:43 pm02 external/stonith-helper[19932]: info: 192.168.102.131 responded.
	Apr 24 06:26:43 pm02 external/stonith-helper[19929]: info: 192.168.122.41 responded.
	Apr 24 06:26:47 pm02 stonith: [19905]: CRIT: external_reset_req: 'stonith-helper reset' for host pm01 failed with rc 1
	Apr 24 06:26:47 pm02 stonith-ng[16428]:    info: Attempted to execute agent fence_legacy (reboot) the maximum number of times (1) allowed
	Apr 24 06:26:47 pm02 stonith-ng[16428]:   error: Operation 'reboot' [19904] (call 2 from crmd.16432) for host 'pm01' with device 'prmStonith1-1' returned: -61 (No data available)
	Apr 24 06:26:47 pm02 stonith-ng[16428]: warning: prmStonith1-1:19904 [ Performing: stonith -t external/stonith-helper -T reset pm01 ]
	Apr 24 06:26:47 pm02 stonith-ng[16428]: warning: prmStonith1-1:19904 [ failed: pm01 5 ]
	Apr 24 06:26:47 pm02 stonith-ng[16428]:  notice: Call to prmStonith1-1 for 'pm01 reboot' on behalf of crmd.16432@pm02: No data available (-61)
⑬	Apr 24 06:26:47 pm02 stonith-ng[16428]:    info: Requesting that 'pm02' perform op 'pm01 reboot' with 'prmStonith1-2' for crmd.16432 (72s)
	Apr 24 06:26:48 pm02 cib[16427]:    info: Reporting our current digest to pm02: fbc9ceefd5f79f6a94f7493f17370f61 for 0.6.22 (0x7f466c41ae50 0)
	Apr 24 06:26:48 pm02 external/libvirt[20063]: notice: Domain pm01 was stopped
	Apr 24 06:26:49 pm02 corosync[16413]: [TOTEM ] A processor failed, forming new configuration.
	Apr 24 06:26:50 pm02 corosync[16413]: [TOTEM ] A new membership (192.168.101.132:528) was formed. Members left: 3232261507
	Apr 24 06:26:50 pm02 corosync[16413]: [TOTEM ] Failed to receive the leave message. failed: 3232261507
	Apr 24 06:26:50 pm02 corosync[16413]: [QUORUM] This node is within the non-primary component and will NOT provide any services.
	Apr 24 06:26:50 pm02 corosync[16413]: [QUORUM] Members[1]: 3232261508
	Apr 24 06:26:50 pm02 corosync[16413]: [MAIN  ] Completed service synchronization, ready to provide service.
	Apr 24 06:26:50 pm02 attrd[16430]:    info: Node 3232261507 left group attrd (peer=pm01, counter=3.0)
	Apr 24 06:26:50 pm02 attrd[16430]:    info: pcmk_cpg_membership: Node pm01[3232261507] - corosync-cpg is now offline
	Apr 24 06:26:50 pm02 attrd[16430]:  notice: Node pm01 state is now lost
	Apr 24 06:26:50 pm02 attrd[16430]:  notice: Removing all pm01 attributes for peer loss
	Apr 24 06:26:50 pm02 attrd[16430]:    info: Removing node with name pm01 and id 3232261507 from membership cache
	Apr 24 06:26:50 pm02 attrd[16430]:  notice: Purged 1 peers with id=3232261507 and/or uname=pm01 from the membership cache
	Apr 24 06:26:50 pm02 attrd[16430]:    info: Node 3232261508 still member of group attrd (peer=pm02, counter=3.0)
	Apr 24 06:26:50 pm02 crmd[16432]: warning: Quorum lost
	Apr 24 06:26:50 pm02 crmd[16432]:  notice: Node pm01 state is now lost
⑭	Apr 24 06:26:50 pm02 crmd[16432]:    info: Cluster node pm01 is now lost (was member)
	Apr 24 06:26:50 pm02 crmd[16432]:    info: reap_dead_nodes: Node pm01[3232261507] - join-2 phase 4 -> 0
	Apr 24 06:26:50 pm02 pacemakerd[16421]: warning: Quorum lost
	Apr 24 06:26:50 pm02 pacemakerd[16421]:  notice: Node pm01 state is now lost
	Apr 24 06:26:50 pm02 pacemakerd[16421]:    info: Node 3232261507 left group pacemakerd (peer=pm01, counter=3.0)
	Apr 24 06:26:50 pm02 pacemakerd[16421]:    info: pcmk_cpg_membership: Node pm01[3232261507] - corosync-cpg is now offline
	Apr 24 06:26:50 pm02 pacemakerd[16421]:    info: Node 3232261508 still member of group pacemakerd (peer=pm02, counter=3.0)
	Apr 24 06:26:50 pm02 cib[16427]:    info: Node 3232261507 left group cib (peer=pm01, counter=3.0)
	Apr 24 06:26:50 pm02 cib[16427]:    info: pcmk_cpg_membership: Node pm01[3232261507] - corosync-cpg is now offline
	Apr 24 06:26:50 pm02 cib[16427]:  notice: Node pm01 state is now lost
	Apr 24 06:26:50 pm02 cib[16427]:    info: Removing node with name pm01 and id 3232261507 from membership cache
	Apr 24 06:26:50 pm02 cib[16427]:  notice: Purged 1 peers with id=3232261507 and/or uname=pm01 from the membership cache
	Apr 24 06:26:50 pm02 cib[16427]:    info: Node 3232261508 still member of group cib (peer=pm02, counter=3.0)
	Apr 24 06:26:50 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/131)
	Apr 24 06:26:50 pm02 stonith-ng[16428]:    info: Node 3232261507 left group stonith-ng (peer=pm01, counter=3.0)
	Apr 24 06:26:50 pm02 stonith-ng[16428]:    info: pcmk_cpg_membership: Node pm01[3232261507] - corosync-cpg is now offline
	Apr 24 06:26:50 pm02 stonith-ng[16428]:  notice: Node pm01 state is now lost
	Apr 24 06:26:50 pm02 pacemakerd[16421]:    info: Ignoring process list sent by peer for local node
	Apr 24 06:26:50 pm02 stonith-ng[16428]:    info: Removing node with name pm01 and id 3232261507 from membership cache
	Apr 24 06:26:50 pm02 stonith-ng[16428]:  notice: Purged 1 peers with id=3232261507 and/or uname=pm01 from the membership cache
	Apr 24 06:26:50 pm02 stonith-ng[16428]:    info: Node 3232261508 still member of group stonith-ng (peer=pm02, counter=3.0)
	Apr 24 06:26:50 pm02 cib[16427]:    info: Forwarding cib_modify operation for section cib to all (origin=local/crmd/132)
	Apr 24 06:26:50 pm02 cib[16427]:    info: Forwarding cib_modify operation for section nodes to all (origin=local/crmd/135)
	Apr 24 06:26:50 pm02 cib[16427]:    info: Diff: --- 0.6.22 2
	Apr 24 06:26:50 pm02 cib[16427]:    info: Diff: +++ 0.6.23 (null)
	Apr 24 06:26:50 pm02 cib[16427]:    info: +  /cib:  @num_updates=23
	Apr 24 06:26:50 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261507']:  @crm-debug-origin=peer_update_callback
	Apr 24 06:26:50 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/131, version=0.6.23)
	Apr 24 06:26:50 pm02 cib[16427]:    info: Diff: --- 0.6.23 2
	Apr 24 06:26:50 pm02 cib[16427]:    info: Diff: +++ 0.6.24 be2acc816a40b82a1c7fc40ee4b82f76
	Apr 24 06:26:50 pm02 cib[16427]:    info: +  /cib:  @num_updates=24, @have-quorum=0
	Apr 24 06:26:50 pm02 cib[16427]:    info: Completed cib_modify operation for section cib: OK (rc=0, origin=pm02/crmd/132, version=0.6.24)
	Apr 24 06:26:50 pm02 cib[16427]:    info: Completed cib_modify operation for section nodes: OK (rc=0, origin=pm02/crmd/135, version=0.6.24)
	Apr 24 06:26:50 pm02 crmd[16432]:    info: Node 3232261507 left group crmd (peer=pm01, counter=3.0)
	Apr 24 06:26:50 pm02 crmd[16432]:    info: pcmk_cpg_membership: Node pm01[3232261507] - corosync-cpg is now offline
	Apr 24 06:26:50 pm02 crmd[16432]:    info: Client pm01/peer now has status [offline] (DC=true, changed=4000000)
	Apr 24 06:26:50 pm02 crmd[16432]:    info: Peer pm01 left us
	Apr 24 06:26:50 pm02 crmd[16432]:    info: Deleting xpath: //node_state[@uname='pm01']/transient_attributes
	Apr 24 06:26:50 pm02 crmd[16432]:    info: Node 3232261508 still member of group crmd (peer=pm02, counter=3.0)
	Apr 24 06:26:50 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/136)
	Apr 24 06:26:50 pm02 cib[16427]:    info: Forwarding cib_delete operation for section //node_state[@uname='pm01']/transient_attributes to all (origin=local/crmd/137)
	Apr 24 06:26:50 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/138)
	Apr 24 06:26:50 pm02 cib[16427]:    info: Diff: --- 0.6.24 2
	Apr 24 06:26:50 pm02 cib[16427]:    info: Diff: +++ 0.6.25 (null)
	Apr 24 06:26:50 pm02 cib[16427]:    info: +  /cib:  @num_updates=25
	Apr 24 06:26:50 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261508']:  @crm-debug-origin=post_cache_update
	Apr 24 06:26:50 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261507']:  @in_ccm=false, @crm-debug-origin=post_cache_update
	Apr 24 06:26:50 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/136, version=0.6.25)
	Apr 24 06:26:50 pm02 cib[16427]:    info: Diff: --- 0.6.25 2
	Apr 24 06:26:50 pm02 cib[16427]:    info: Diff: +++ 0.6.26 (null)
	Apr 24 06:26:50 pm02 cib[16427]:    info: -- /cib/status/node_state[@id='3232261507']/transient_attributes[@id='3232261507']
	Apr 24 06:26:50 pm02 cib[16427]:    info: +  /cib:  @num_updates=26
	Apr 24 06:26:50 pm02 cib[16427]:    info: Completed cib_delete operation for section //node_state[@uname='pm01']/transient_attributes: OK (rc=0, origin=pm02/crmd/137, version=0.6.26)
	Apr 24 06:26:50 pm02 cib[16427]:    info: Diff: --- 0.6.26 2
	Apr 24 06:26:50 pm02 cib[16427]:    info: Diff: +++ 0.6.27 (null)
	Apr 24 06:26:50 pm02 cib[16427]:    info: +  /cib:  @num_updates=27
	Apr 24 06:26:50 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261507']:  @crmd=offline, @crm-debug-origin=peer_update_callback
	Apr 24 06:26:50 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/138, version=0.6.27)
	Apr 24 06:26:51 pm02 external/libvirt[20063]: notice: Domain pm01 was started
	Apr 24 06:26:52 pm02 stonith-ng[16428]:  notice: Operation 'reboot' [20056] (call 2 from crmd.16432) for host 'pm01' with device 'prmStonith1-2' returned: 0 (OK)
⑮	Apr 24 06:26:52 pm02 stonith-ng[16428]:  notice: Call to prmStonith1-2 for 'pm01 reboot' on behalf of crmd.16432@pm02: OK (0)
	Apr 24 06:26:52 pm02 stonith-ng[16428]:  notice: Operation reboot of pm01 by pm02 for crmd.16432@pm02.4f64bf61: OK
	Apr 24 06:26:52 pm02 crmd[16432]:  notice: Stonith operation 2/65:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf: OK (0)
	Apr 24 06:26:52 pm02 crmd[16432]:    info: crmd_peer_down: Node pm01[3232261507] - expected state is now down (was member)
	Apr 24 06:26:52 pm02 crmd[16432]:    info: Deleting xpath: //node_state[@uname='pm01']/lrm
	Apr 24 06:26:52 pm02 crmd[16432]:    info: Deleting xpath: //node_state[@uname='pm01']/transient_attributes
⑯	Apr 24 06:26:52 pm02 crmd[16432]:  notice: Peer pm01 was terminated (reboot) by pm02 for pm02: OK (ref=4f64bf61-9b88-4934-853b-704424f6d7de) by client crmd.16432
	Apr 24 06:26:52 pm02 crmd[16432]:    info: Deleting xpath: //node_state[@uname='pm01']/lrm
	Apr 24 06:26:52 pm02 crmd[16432]:    info: Deleting xpath: //node_state[@uname='pm01']/transient_attributes
	Apr 24 06:26:52 pm02 crmd[16432]:  notice: Initiating start operation prmEx_start_0 locally on pm02
	Apr 24 06:26:52 pm02 crmd[16432]:    info: Performing key=14:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf op=prmEx_start_0
	Apr 24 06:26:52 pm02 lrmd[16429]:    info: executing - rsc:prmEx action:start call_id:92
	Apr 24 06:26:52 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/139)
	Apr 24 06:26:52 pm02 cib[16427]:    info: Forwarding cib_delete operation for section //node_state[@uname='pm01']/lrm to all (origin=local/crmd/140)
	Apr 24 06:26:52 pm02 cib[16427]:    info: Forwarding cib_delete operation for section //node_state[@uname='pm01']/transient_attributes to all (origin=local/crmd/141)
	Apr 24 06:26:52 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/142)
	Apr 24 06:26:52 pm02 cib[16427]:    info: Forwarding cib_delete operation for section //node_state[@uname='pm01']/lrm to all (origin=local/crmd/143)
	Apr 24 06:26:52 pm02 cib[16427]:    info: Diff: --- 0.6.27 2
	Apr 24 06:26:52 pm02 cib[16427]:    info: Diff: +++ 0.6.28 (null)
	Apr 24 06:26:52 pm02 cib[16427]:    info: +  /cib:  @num_updates=28
	Apr 24 06:26:52 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261507']:  @crm-debug-origin=send_stonith_update, @join=down, @expected=down
	Apr 24 06:26:52 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/139, version=0.6.28)
	Apr 24 06:26:52 pm02 cib[16427]:    info: Diff: --- 0.6.28 2
	Apr 24 06:26:52 pm02 cib[16427]:    info: Diff: +++ 0.6.29 (null)
	Apr 24 06:26:52 pm02 cib[16427]:    info: -- /cib/status/node_state[@id='3232261507']/lrm[@id='3232261507']
	Apr 24 06:26:52 pm02 cib[16427]:    info: +  /cib:  @num_updates=29
	Apr 24 06:26:52 pm02 cib[16427]:    info: Completed cib_delete operation for section //node_state[@uname='pm01']/lrm: OK (rc=0, origin=pm02/crmd/140, version=0.6.29)
	Apr 24 06:26:52 pm02 cib[16427]:    info: Completed cib_delete operation for section //node_state[@uname='pm01']/transient_attributes: OK (rc=0, origin=pm02/crmd/141, version=0.6.29)
	Apr 24 06:26:52 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/142, version=0.6.29)
	Apr 24 06:26:52 pm02 cib[16427]:    info: Completed cib_delete operation for section //node_state[@uname='pm01']/lrm: OK (rc=0, origin=pm02/crmd/143, version=0.6.29)
	Apr 24 06:26:52 pm02 cib[16427]:    info: Forwarding cib_delete operation for section //node_state[@uname='pm01']/transient_attributes to all (origin=local/crmd/144)
	Apr 24 06:26:52 pm02 crmd[16432]:    info: Fencing update 139 for pm01: complete
	Apr 24 06:26:52 pm02 crmd[16432]:    info: Fencing update 142 for pm01: complete
	Apr 24 06:26:52 pm02 cib[16427]:    info: Completed cib_delete operation for section //node_state[@uname='pm01']/transient_attributes: OK (rc=0, origin=pm02/crmd/144, version=0.6.29)
	Apr 24 06:26:52 pm02 sfex(prmEx)[20118]: INFO: sfex_daemon: starting...
	Apr 24 06:26:52 pm02 sfex_daemon: [20128]: info: Starting SFeX Daemon...
	Apr 24 06:26:57 pm02 cib[16427]:    info: Reporting our current digest to pm02: 06e1188561975e8138fc642ae1506540 for 0.6.29 (0x7f466c3c6910 0)
	Apr 24 06:28:03 pm02 sfex_daemon: [20128]: info: lock acquired
	Apr 24 06:28:03 pm02 sfex_daemon: [20435]: info: SFeX Daemon started.
	Apr 24 06:28:03 pm02 sfex(prmEx)[20118]: INFO: sfex_daemon: started.
	Apr 24 06:28:03 pm02 lrmd[16429]:    info: finished - rsc:prmEx action:start call_id:92 pid:20118 exit-code:0 exec-time:71161ms queue-time:0ms
	Apr 24 06:28:03 pm02 crmd[16432]:    info: Managed sfex_meta-data_0 process 20443 exited with rc=0
	Apr 24 06:28:03 pm02 crmd[16432]:  notice: Result of start operation for prmEx on pm02: 0 (ok)
	Apr 24 06:28:03 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/145)
	Apr 24 06:28:03 pm02 cib[16427]:    info: Diff: --- 0.6.29 2
	Apr 24 06:28:03 pm02 cib[16427]:    info: Diff: +++ 0.6.30 (null)
	Apr 24 06:28:03 pm02 cib[16427]:    info: +  /cib:  @num_updates=30
	Apr 24 06:28:03 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261508']:  @crm-debug-origin=do_update_resource
	Apr 24 06:28:03 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmEx']/lrm_rsc_op[@id='prmEx_last_0']:  @operation_key=prmEx_start_0, @operation=start, @transition-key=14:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @transition-magic=0:0;14:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @call-id=92, @last-run=1492982812, @last-rc-change=1492982812, @exec-time=71161
	Apr 24 06:28:03 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/145, version=0.6.30)
	Apr 24 06:28:03 pm02 crmd[16432]:    info: Action prmEx_start_0 (14) confirmed on pm02 (rc=0)
	Apr 24 06:28:03 pm02 crmd[16432]:  notice: Initiating monitor operation prmEx_monitor_10000 locally on pm02
	Apr 24 06:28:03 pm02 crmd[16432]:    info: Performing key=15:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf op=prmEx_monitor_10000
	Apr 24 06:28:03 pm02 crmd[16432]:  notice: Initiating start operation prmFs_start_0 locally on pm02
	Apr 24 06:28:03 pm02 crmd[16432]:    info: Performing key=17:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf op=prmFs_start_0
	Apr 24 06:28:03 pm02 lrmd[16429]:    info: executing - rsc:prmFs action:start call_id:94
	Apr 24 06:28:03 pm02 crmd[16432]:    info: Result of monitor operation for prmEx on pm02: 0 (ok)
	Apr 24 06:28:03 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/146)
	Apr 24 06:28:03 pm02 cib[16427]:    info: Diff: --- 0.6.30 2
	Apr 24 06:28:03 pm02 cib[16427]:    info: Diff: +++ 0.6.31 (null)
	Apr 24 06:28:03 pm02 cib[16427]:    info: +  /cib:  @num_updates=31
	Apr 24 06:28:03 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmEx']/lrm_rsc_op[@id='prmEx_monitor_10000']:  @transition-key=15:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @transition-magic=0:0;15:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @call-id=93, @last-rc-change=1492982883, @exec-time=44
	Apr 24 06:28:03 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/146, version=0.6.31)
	Apr 24 06:28:03 pm02 crmd[16432]:    info: Action prmEx_monitor_10000 (15) confirmed on pm02 (rc=0)
	Apr 24 06:28:03 pm02 Filesystem(prmFs)[20448]: INFO: Running start for /dev/vdb2 on /dbfp
	Apr 24 06:28:03 pm02 Filesystem(prmFs)[20448]: INFO: Starting filesystem check on /dev/vdb2
	Apr 24 06:28:03 pm02 lrmd[16429]:    info: finished - rsc:prmFs action:start call_id:94 pid:20448 exit-code:0 exec-time:225ms queue-time:0ms
	Apr 24 06:28:03 pm02 crmd[16432]:    info: Managed Filesystem_meta-data_0 process 20523 exited with rc=0
	Apr 24 06:28:03 pm02 crmd[16432]:  notice: Result of start operation for prmFs on pm02: 0 (ok)
	Apr 24 06:28:03 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/147)
	Apr 24 06:28:03 pm02 cib[16427]:    info: Diff: --- 0.6.31 2
	Apr 24 06:28:03 pm02 cib[16427]:    info: Diff: +++ 0.6.32 (null)
	Apr 24 06:28:03 pm02 cib[16427]:    info: +  /cib:  @num_updates=32
	Apr 24 06:28:03 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmFs']/lrm_rsc_op[@id='prmFs_last_0']:  @operation_key=prmFs_start_0, @operation=start, @transition-key=17:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @transition-magic=0:0;17:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @call-id=94, @last-run=1492982883, @last-rc-change=1492982883, @exec-time=225
	Apr 24 06:28:03 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/147, version=0.6.32)
	Apr 24 06:28:03 pm02 crmd[16432]:    info: Action prmFs_start_0 (17) confirmed on pm02 (rc=0)
	Apr 24 06:28:03 pm02 crmd[16432]:  notice: Initiating monitor operation prmFs_monitor_10000 locally on pm02
	Apr 24 06:28:03 pm02 crmd[16432]:    info: Performing key=18:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf op=prmFs_monitor_10000
	Apr 24 06:28:03 pm02 crmd[16432]:  notice: Initiating start operation prmIp_start_0 locally on pm02
	Apr 24 06:28:03 pm02 crmd[16432]:    info: Performing key=20:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf op=prmIp_start_0
	Apr 24 06:28:03 pm02 lrmd[16429]:    info: executing - rsc:prmIp action:start call_id:96
	Apr 24 06:28:03 pm02 crmd[16432]:    info: Result of monitor operation for prmFs on pm02: 0 (ok)
	Apr 24 06:28:03 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/148)
	Apr 24 06:28:03 pm02 cib[16427]:    info: Diff: --- 0.6.32 2
	Apr 24 06:28:03 pm02 cib[16427]:    info: Diff: +++ 0.6.33 (null)
	Apr 24 06:28:03 pm02 cib[16427]:    info: +  /cib:  @num_updates=33
	Apr 24 06:28:03 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmFs']/lrm_rsc_op[@id='prmFs_monitor_10000']:  @transition-key=18:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @transition-magic=0:0;18:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @call-id=95, @last-rc-change=1492982883, @exec-time=113
	Apr 24 06:28:03 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/148, version=0.6.33)
	Apr 24 06:28:03 pm02 crmd[16432]:    info: Action prmFs_monitor_10000 (18) confirmed on pm02 (rc=0)
	Apr 24 06:28:04 pm02 IPaddr2(prmIp)[20530]: INFO: Adding inet address 192.168.201.100/24 with broadcast address 192.168.201.255 to device eth1
	Apr 24 06:28:04 pm02 IPaddr2(prmIp)[20530]: INFO: Bringing device eth1 up
	Apr 24 06:28:04 pm02 IPaddr2(prmIp)[20530]: INFO: /usr/lib64/heartbeat/send_arp -i 200 -r 5 -p /var/run/resource-agents/send_arp-192.168.201.100 eth1 192.168.201.100 auto not_used not_used
	Apr 24 06:28:04 pm02 lrmd[16429]:    info: finished - rsc:prmIp action:start call_id:96 pid:20530 exit-code:0 exec-time:158ms queue-time:0ms
	Apr 24 06:28:04 pm02 crmd[16432]:    info: Managed IPaddr2_meta-data_0 process 20645 exited with rc=0
	Apr 24 06:28:04 pm02 crmd[16432]:  notice: Result of start operation for prmIp on pm02: 0 (ok)
	Apr 24 06:28:04 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/149)
	Apr 24 06:28:04 pm02 cib[16427]:    info: Diff: --- 0.6.33 2
	Apr 24 06:28:04 pm02 cib[16427]:    info: Diff: +++ 0.6.34 (null)
	Apr 24 06:28:04 pm02 cib[16427]:    info: +  /cib:  @num_updates=34
	Apr 24 06:28:04 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmIp']/lrm_rsc_op[@id='prmIp_last_0']:  @operation_key=prmIp_start_0, @operation=start, @transition-key=20:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @transition-magic=0:0;20:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @call-id=96, @last-run=1492982883, @last-rc-change=1492982883, @exec-time=158
	Apr 24 06:28:04 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/149, version=0.6.34)
	Apr 24 06:28:04 pm02 crmd[16432]:    info: Action prmIp_start_0 (20) confirmed on pm02 (rc=0)
	Apr 24 06:28:04 pm02 crmd[16432]:  notice: Initiating monitor operation prmIp_monitor_10000 locally on pm02
	Apr 24 06:28:04 pm02 crmd[16432]:    info: Performing key=21:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf op=prmIp_monitor_10000
	Apr 24 06:28:04 pm02 crmd[16432]:  notice: Initiating start operation prmPg_start_0 locally on pm02
	Apr 24 06:28:04 pm02 crmd[16432]:    info: Performing key=23:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf op=prmPg_start_0
	Apr 24 06:28:04 pm02 lrmd[16429]:    info: executing - rsc:prmPg action:start call_id:98
	Apr 24 06:28:04 pm02 crmd[16432]:    info: Result of monitor operation for prmIp on pm02: 0 (ok)
	Apr 24 06:28:04 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/150)
	Apr 24 06:28:04 pm02 cib[16427]:    info: Diff: --- 0.6.34 2
	Apr 24 06:28:04 pm02 cib[16427]:    info: Diff: +++ 0.6.35 (null)
	Apr 24 06:28:04 pm02 cib[16427]:    info: +  /cib:  @num_updates=35
	Apr 24 06:28:04 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmIp']/lrm_rsc_op[@id='prmIp_monitor_10000']:  @transition-key=21:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @transition-magic=0:0;21:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @call-id=97, @last-rc-change=1492982884, @exec-time=142
	Apr 24 06:28:04 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/150, version=0.6.35)
	Apr 24 06:28:04 pm02 crmd[16432]:    info: Action prmIp_monitor_10000 (21) confirmed on pm02 (rc=0)
	Apr 24 06:28:04 pm02 pgsql(prmPg)[20651]: ERROR: command failed: runuser postgres -c cd /dbfp/pgdata/data; kill -s 0 8735 >/dev/null 2>&1
	Apr 24 06:28:04 pm02 pgsql(prmPg)[20651]: INFO: server starting
	Apr 24 06:28:04 pm02 pgsql(prmPg)[20651]: INFO: PostgreSQL start command sent.
	Apr 24 06:28:04 pm02 pgsql(prmPg)[20651]: WARNING: psql: FATAL: the database system is starting up
	Apr 24 06:28:04 pm02 pgsql(prmPg)[20651]: WARNING: PostgreSQL template1 isn't running. rc=2
	Apr 24 06:28:04 pm02 pgsql(prmPg)[20651]: WARNING: Connection error (connection to the server went bad and the session was not interactive) occurred while executing the psql command.
	Apr 24 06:28:05 pm02 pgsql(prmPg)[20651]: INFO: PostgreSQL is started.
	Apr 24 06:28:05 pm02 lrmd[16429]:    info: finished - rsc:prmPg action:start call_id:98 pid:20651 exit-code:0 exec-time:1557ms queue-time:0ms
	Apr 24 06:28:05 pm02 crmd[16432]:    info: Managed pgsql_meta-data_0 process 20895 exited with rc=0
	Apr 24 06:28:05 pm02 crmd[16432]:  notice: Result of start operation for prmPg on pm02: 0 (ok)
	Apr 24 06:28:05 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/151)
	Apr 24 06:28:05 pm02 cib[16427]:    info: Diff: --- 0.6.35 2
	Apr 24 06:28:05 pm02 cib[16427]:    info: Diff: +++ 0.6.36 (null)
	Apr 24 06:28:05 pm02 cib[16427]:    info: +  /cib:  @num_updates=36
	Apr 24 06:28:05 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmPg']/lrm_rsc_op[@id='prmPg_last_0']:  @operation_key=prmPg_start_0, @operation=start, @transition-key=23:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @transition-magic=0:0;23:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @call-id=98, @last-run=1492982884, @last-rc-change=1492982884, @exec-time=1557
	Apr 24 06:28:05 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/151, version=0.6.36)
	Apr 24 06:28:05 pm02 crmd[16432]:    info: Action prmPg_start_0 (23) confirmed on pm02 (rc=0)
	Apr 24 06:28:05 pm02 crmd[16432]:  notice: Initiating monitor operation prmPg_monitor_10000 locally on pm02
	Apr 24 06:28:05 pm02 crmd[16432]:    info: Performing key=24:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf op=prmPg_monitor_10000
	Apr 24 06:28:05 pm02 crmd[16432]:    info: Result of monitor operation for prmPg on pm02: 0 (ok)
	Apr 24 06:28:05 pm02 cib[16427]:    info: Forwarding cib_modify operation for section status to all (origin=local/crmd/152)
	Apr 24 06:28:05 pm02 cib[16427]:    info: Diff: --- 0.6.36 2
	Apr 24 06:28:05 pm02 cib[16427]:    info: Diff: +++ 0.6.37 (null)
	Apr 24 06:28:05 pm02 cib[16427]:    info: +  /cib:  @num_updates=37
	Apr 24 06:28:05 pm02 cib[16427]:    info: +  /cib/status/node_state[@id='3232261508']/lrm[@id='3232261508']/lrm_resources/lrm_resource[@id='prmPg']/lrm_rsc_op[@id='prmPg_monitor_10000']:  @transition-key=24:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @transition-magic=0:0;24:17:0:22827238-3a1c-41e1-a1b5-75a7e8ac21cf, @call-id=99, @last-rc-change=1492982885, @exec-time=178
	Apr 24 06:28:05 pm02 cib[16427]:    info: Completed cib_modify operation for section status: OK (rc=0, origin=pm02/crmd/152, version=0.6.37)
	Apr 24 06:28:05 pm02 crmd[16432]:    info: Action prmPg_monitor_10000 (24) confirmed on pm02 (rc=0)
	Apr 24 06:28:05 pm02 crmd[16432]:  notice: Transition 17 (Complete=32, Pending=0, Fired=0, Skipped=0, Incomplete=0, Source=/var/lib/pacemaker/pengine/pe-warn-1.bz2): Complete
	Apr 24 06:28:05 pm02 crmd[16432]:    info: Input I_TE_SUCCESS received in state S_TRANSITION_ENGINE from notify_crmd
	Apr 24 06:28:05 pm02 crmd[16432]:  notice: State transition S_TRANSITION_ENGINE -> S_IDLE
	Apr 24 06:28:10 pm02 cib[16427]:    info: Reporting our current digest to pm02: 079af295fe262bff278aa42475f4bf2f for 0.6.37 (0x7f466c3c6910 0)
```
