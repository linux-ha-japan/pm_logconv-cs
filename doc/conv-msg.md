# Pacemakerログ解析支援ツール（変換後ログメッセージ一覧）

- [Pacemakerサービス起動時のメッセージ一覧](#pacemakerサービス起動時のメッセージ一覧)
- [Pacemakerサービス終了時のメッセージ一覧](#pacemakerサービス終了時のメッセージ一覧)
- [Pacemakerプロセス制御のメッセージ一覧](#pacemakerプロセス制御のメッセージ一覧)
- [ノード状態変更時のメッセージ一覧](#ノード状態変更時のメッセージ一覧)
- [DC遷移時のメッセージ一覧](#dc遷移時のメッセージ一覧)
- [リソース監視・制御時のメッセージ一覧](#リソース監視制御時のメッセージ一覧)
- [リソース移行時のメッセージ一覧](#リソース移行時のメッセージ一覧)
- [インターコネクトLAN状態変更時のメッセージ一覧](#インターコネクトlan状態変更時のメッセージ一覧)
- [ネットワーク監視故障検知時のメッセージ一覧](#ネットワーク監視故障検知時のメッセージ一覧)
- [ディスク監視故障検知時のメッセージ一覧](#ディスク監視故障検知時のメッセージ一覧)
- [属性変更時のメッセージ一覧](#属性変更時のメッセージ一覧)
- [STONITHリソース監視・制御時のメッセージ一覧](#stonithリソース監視制御時のメッセージ一覧)
- [STONITH実行時のメッセージ一覧](#stonith実行時のメッセージ一覧)
- [フェイルオーバの開始を表すメッセージ一覧](#フェイルオーバの開始を表すメッセージ一覧)
- [フェイルオーバの完了を表すメッセージ一覧](#フェイルオーバの完了を表すメッセージ一覧)
- [フェイルオーバ中のリソース状態を表すメッセージ一覧](#フェイルオーバ中のリソース状態を表すメッセージ一覧)

***
※ 表中の「**No**」は、ツール内部で使用している番号です(開発者向け)。ユーザが本番号を意識するケースはありません。

## Pacemakerサービス起動時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| 23-1	| サービス起動 Corosync				| corosync[31153]: [MAIN  ] Corosync Cluster Engine ('*2.4.2*'): started and ready to provide service.	| info	|Starting Corosync *2.4.2*.	| Corosync *2.4.2* を起動します。	|
| 23-4	| サービス起動 Pacemaker			| pacemakerd[31160]:  notice: Starting Pacemaker *1.1.17-1.el7*						| info	|Starting Pacemaker *1.1.17*.	| Pacemaker *1.1.17* を起動します。	|

## Pacemakerサービス終了時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| 14-1	| サービス終了 Corosync停止開始			| corosync[31154]: [SERV  ] Unloading all Corosync service engines.		| info	| Corosync is shutting down.		| Corosyncが停止処理を開始します。	|
| 14-2	| サービス終了 Corosync停止完了			| corosync[31154]: [MAIN  ] Corosync Cluster Engine exiting normally		| info	| Corosync shutdown complete.		| Corosyncの停止処理が完了しました。	|
| 14-3	| サービス終了 Pacemaker停止開始		| pacemakerd[31160]:  notice: Shutting down Pacemaker				| info	| Pacemaker is shutting down.		| Pacemakerが停止処理を開始します。	|
| 14-4	| サービス終了 Pacemaker停止完了		| pacemakerd[31160]:  notice: Shutdown complete					| info	| Pacemaker shutdown complete.		| Pacemakerの停止処理が完了しました。	|
| 14-5	| サービス終了 Pacemaker停止中			| crmd[31169]:    info: Creating shutdown request for *pm02* (state=*S_IDLE*)	| info	| Pacemaker on *pm02* is shutting down.	| ノード*pm02*上の、Pacemakerが停止処理を行ってます。<br>※本ログはDCノードでのみ出力されます。	|

## Pacemakerプロセス制御のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| 10-1	| プロセス状態 起動				| pacemakerd[31160]:    info: Forked child *31164* for process *cib*							| info	| Start "*cib*" process. (pid=*31164*)				| *cib*プロセスが起動しました。(PID=*31164*)			|
| 10-2	| プロセス状態 異常終了(エラー発生による終了①)	| pacemakerd[24012]:   error: The *crmd* process (*24021*) exited: *Generic Pacemaker error* (*201*)			| warning| Managed "*crmd*" process exited. (pid=*24021*, rc=*201*)	| *crmd*プロセス(PID=*24021*)が終了コード*201*で終了しました。	|
| 10-4	| プロセス状態 異常終了(エラー発生による終了②)	| pacemakerd[16364]: warning: The *crmd* process (*16373*) can no longer be respawned, shutting the cluster down.	| warning| Managed "*crmd*" process exited. (pid=*16373*, rc=*100*)	| *crmd*プロセス(PID=*16373*)が、終了コード*100*で終了しました。|
| 10-5	| プロセス状態 異常終了(エラー発生による終了③)	| pacemakerd[8627]:   emerg: The *crmd* process (*8635*) instructed the machine to reset				| warning| Managed "*crmd*" process exited. (pid=*8635*, rc=*255*)	| *crmd*プロセス(PID=*8635*)が、終了コード*255*で終了しました。	|
| 10-3	| プロセス状態 異常終了(シグナルによる終了)	| (1. SIGKILLによる終了)<br>pacemakerd[24012]: warning: The *cib* process (*24016*) terminated with signal *9* (core=*0*)<br>(2. SIGKILL以外のシグナルによる終了)<br>pacemakerd[9746]:   error: The *cib* process (*9750*) terminated with signal *1* (core=*0*)	| warning| (1)<br>Managed "*cib*" process terminated with signal *9*. (pid=*24016*)<br>(2)<br>Managed "*cib*" process terminated with signal *1*. (pid=*9750*)	| (1)<br>*cib*プロセス(PID=*24016*)がシグナル*9*番によって停止しました。<br>(2)<br>*cib*プロセス(PID=*9750*)がシグナル*1*番によって停止しました。	|
| 10-6	| プロセス状態 正常終了				| pacemakerd[31160]:    info: The *cib* process (*31164*) exited: OK (0)						| info	| Stop "*cib*" process normally. (pid=*31164*)			| *cib*プロセス(PID=*31164*)が正常に終了しました。		|
| 10-7	| プロセス状態 複数回異常終了			| pacemakerd[30354]:   error: Child respawn count exceeded by *stonith-ng*						| error	| Respawn count exceeded by "*stonith-ng*".			| *stonith-ng*プロセスが再起動回数を超過しました。		|

## ノード状態変更時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| 6-1	| ノード状態 離脱				| crmd[1404]:    info: Cluster node *pm01* is now lost (was member)									| warning| Node *pm01* is lost	| ノード*pm01*がクラスタメンバシップから離脱しました。	|
| 6-2	| ノード状態 参加				| crmd[8623]:    info: Cluster node *pm01* is now member<br>または<br>crmd[31169]:    info: Cluster node *pm01* is now member (was in unknown state)	| info	| Node *pm01* is member	| ノード*pm01*がクラスタメンバシップに参加しました。	|

## DC遷移時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| 13-2	| DC遷移 選出					| crmd[31169]:    info: Set DC to *pm01* (*3.0.11*)	| info	| Set DC node to *pm01*.	| ノード*pm01*がDCノードに選出されました。	|
| 13-5	| DC遷移 剥奪					| crmd[8623]:    info: Unset DC. Was *pm01*		| info	| Unset DC node *pm01*.		| ノード*pm01*がDCノードではなくなりました。	|

## リソース監視・制御時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| 1-1	| リソース起動 開始				| crmd[31169]:    info: Performing key=*36:0:0:5a50acfd-4843-4ca6-a3bc-be254cc81a6e* op=*prmResource*_start_0	| info	| Resource *prmResource* tries to start.				| *prmResource*を起動(start)します。						|
| 1-2	| リソース起動 終了(成功)			| crmd[31169]:  notice: Result of start operation for *prmResource* on *pm01*: 0 (ok)				| info	| Resource *prmResource* started. (rc=0) ok				| *prmResource*の起動(start)が正常に終了しました。				|
| 1-3	| リソース起動 終了(エラー)			| crmd[18806]:  notice: Result of start operation for *prmResource* on *pm01*: *1* (*unknown error*)		| error	| Resource *prmResource* failed to start. (rc=*1*) *unknown error*	| *prmResource*の起動(start)でエラーが発生しました。				|
| 1-4	| リソース起動 終了(タイムアウト)		| crmd[32231]:   error: Result of start operation for *prmResource* on *pm01*: Timed Out			| error	| Resource *prmResource* failed to start. (Timed Out)			| *prmResource*の起動(start)でタイムアウトが発生しました。			|
| 2-1	| リソース停止 開始				| crmd[31169]:    info: Performing key=*19:11:0:5a50acfd-4843-4ca6-a3bc-be254cc81a6e* op=*prmResource*_stop_0	| info	| Resource *prmResource* tries to stop.					| *prmResource*を停止(stop)します。						|
| 2-2	| リソース停止 終了(成功)			| crmd[31169]:  notice: Result of stop operation for *prmResource* on *pm01*: 0 (ok)				| info	| Resource *prmResource* stopped. (rc=0) ok				| *prmResource*の停止(stop)が正常に終了しました。				|
| 2-3	| リソース停止 終了(エラー)			| crmd[9457]:  notice: Result of stop operation for *prmResource* on *pm01*: *1* (*unknown error*)		| error	| Resource *prmResource* failed to stop. (rc=*1*) *unknown error*	| *prmResource*の停止(stop)でエラーが発生しました。				|
| 2-4	| リソース停止 終了(タイムアウト)		| crmd[6529]:   error: Result of stop operation for *prmResource* on *pm01*: Timed Out				| error	| Resource *prmResource* failed to stop. (Timed Out)			| *prmResource*の停止(stop)でタイムアウトが発生しました。			|
| 3-1	| リソース監視 終了(エラー)			| crmd[6475]:    info: Result of monitor operation for *prmResource* on *pm01*: *1* (*unknown error*)		| error	| Resource *prmResource* failed to monitor. (rc=*1*) *unknown error*	| *prmResource*の監視(monitor)で故障が発生していることを検知しました。		|
| 3-2	| リソース監視 終了(停止検知)			| crmd[6387]:    info: Result of monitor operation for *prmResource* on *pm01*: 7 (not running)			| error	| Resource *prmResource* does not work. (rc=7) not running		| *prmResource*の監視(monitor)でリソースが停止していることを検知しました。	|
| 3-3	| リソース監視 終了(タイムアウト)		| crmd[14390]:   error: Result of monitor operation for *prmResource* on *pm01*: Timed Out			| error	| Resource *prmResource* failed to monitor. (Timed Out)			| *prmResource*の監視(monitor)でタイムアウトが発生しました。			|
| 4-1	| リソースMaster化 開始				| crmd[31169]:    info: Performing key=*39:6:0:5a50acfd-4843-4ca6-a3bc-be254cc81a6e* op=*prmResource*_promote_0	| info	| Resource *prmResource* tries to promote.				| *prmResource*をMaster化(promote)します。					|
| 4-2	| リソースMaster化 終了(成功)			| crmd[31169]:  notice: Result of promote operation for *prmResource* on *pm01*: 0 (ok)				| info	| Resource *prmResource* promoted. (rc=0) ok				| *prmResource*のMaster化(promote)が正常に終了しました。			|
| 4-3	| リソースMaster化 終了(エラー)			| crmd[25809]:  notice: Result of promote operation for *prmResource* on *pm01*: *1* (*unknown error*)		| error	| Resource *prmResource* failed to promote. (rc=*1*) *unknown error*	| *prmResource*のMaster化(promote)でエラーが発生しました。			|
| 4-4	| リソースMaster化 終了(タイムアウト)		| crmd[32042]:   error: Result of promote operation for *prmResource* on *pm01*: Timed Out			| error	| Resource *prmResource* failed to promote. (Timed Out)			| *prmResource*のMaster化(promote)でタイムアウトが発生しました。		|
| 5-1	| リソースSlave化 開始				| crmd[31169]:    info: Performing key=*44:11:0:5a50acfd-4843-4ca6-a3bc-be254cc81a6e* op=*prmResource*_demote_0	| info	| Resource *prmResource* tries to demote.				| *prmResource*をSlave化(demote)します。					|
| 5-2	| リソースSlave化 終了(成功)			| crmd[31169]:  notice: Result of demote operation for *prmResource* on *pm01*: 0 (ok)				| info	| Resource *prmResource* demoted. (rc=0) ok				| *prmResource*のSlave化(demote)が正常に終了しました。				|
| 5-3	| リソースSlave化 終了(エラー)			| crmd[6118]:  notice: Result of demote operation for *prmResource* on *pm01*: *1* (*unknown error*)		| error	| Resource *prmResource* failed to demote. (rc=*1*) *unknown error*	| *prmResource*のSlave化(demote)でエラーが発生しました。			|
| 5-4	| リソースSlave化 終了(タイムアウト)		| crmd[6336]:   error: Result of demote operation for *prmResource* on *pm01*: Timed Out			| error	| Resource *prmResource* failed to demote. (Timed Out)			| *prmResource*のSlave化(demote)でタイムアウトが発生しました。			|

## リソース移行時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| 11-1	| リソース移行(migrate_to) 開始			| crmd[6691]:    info: Performing key=*22:12:0:e13dcf24-6449-46a2-acbe-c69187f41539* op=*prmResource*_migrate_to_0	| info	| Resource *prmResource* tries to migrate_to.					| *prmResource*を移行(migrate_to)します。				|
| 11-2	| リソース移行(migrate_to) 終了(成功)		| crmd[6691]:  notice: Result of migrate_to operation for *prmResource* on *pm01*: 0 (ok)				| info	| Resource *prmResource* migrated_to. (rc=0) ok					| *prmResource*の移行(migrate_to)が正常に終了しました。			|
| 11-3	| リソース移行(migrate_to) 終了(エラー)		| crmd[13234]:  notice: Result of migrate_to operation for *prmResource* on *pm01*: *1* (*unknown error*)		| error	| Resource *prmResource* failed to migrate_to. (rc=*1*) *unknown error*		| *prmResource*の移行(migrate_to)でエラーが発生しました。		|
| 11-4	| リソース移行(migrate_to) 終了(タイムアウト)	| crmd[19780]:   error: Result of migrate_to operation for *prmResource* on *pm01*: Timed Out				| error	| Resource *prmResource* failed to migrate_to. (Timed Out)			| *prmResource*の移行(migrate_to)でタイムアウトが発生しました。		|
| 12-1	| リソース移行(migrate_from) 開始		| crmd[14239]:    info: Performing key=*23:12:0:e13dcf24-6449-46a2-acbe-c69187f41539* op=*prmResource*_migrate_from_0	| info	| Resource *prmResource* tries to migrate_from.					| *prmResource*を移行(migrate_from)します。				|
| 12-2	| リソース移行(migrate_from) 終了(成功)		| crmd[14239]:  notice: Result of migrate_from operation for *prmResource* on *pm01*: 0 (ok)				| info	| Resource *prmResource* migrated_from. (rc=0) ok				| *prmResource*の移行(migrate_from)が正常に終了しました。		|
| 12-3	| リソース移行(migrate_from) 終了(エラー)	| crmd[24474]:  notice: Result of migrate_from operation for *prmResource* on *pm01*: *1* (*unknown error*)		| error	| Resource *prmResource* failed to migrate_from. (rc=*1*) *unknown error*	| *prmResource*の移行(migrate_from)でエラーが発生しました。		|
| 12-4	| リソース移行(migrate_from) 終了(タイムアウト)	| crmd[29987]:   error: Result of migrate_from operation for *prmResource* on *pm01*: Timed Out				| error	| Resource *prmResource* failed to migrate_from. (Timed Out)			| *prmResource*の移行(migrate_from)でタイムアウトが発生しました。	|

## インターコネクトLAN状態変更時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| 7-1	| インターコネクトLAN状態 故障検知		| corosync[25418]: [TOTEM ] Marking seqid *11906* ringid *0* interface *192.168.101.1* FAULTY	| warning| Ring number *0* is FAULTY (interface *192.168.101.1*).	| インターコネクトLAN *192.168.101.1* (リングナンバー *0*)の故障/停止を検知しました。	|
| 7-2	| インターコネクトLAN状態 回復検知		| corosync[25418]: [TOTEM ] Automatically recovered ring *0*					| info	| Ring number *0* is recovered.					| インターコネクトLAN(リングナンバー *0*)の回復を検知しました。				|

## ネットワーク監視故障検知時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| 8-1	| ネットワーク監視 故障検知			| ping(*prmPing*)[13509]: WARNING: *192.168.201.254* is inactive: PING *192.168.201.254* (*192.168.201.254*) 56(84) bytes of data.#012#012--- *192.168.201.254* ping statistics ---#0122 packets transmitted, 0 received, 100% packet loss, time *1005*ms	| error	| Network to *192.168.201.254* is unreachable.	| ネットワーク監視が故障を検知しました。<br>(監視先IPアドレス *192.168.201.254* に対して通信できませんでした)	|
- ネットワーク監視が"正常である"ことを検知した際には、「[属性変更時のメッセージ一覧](#属性変更時のメッセージ一覧) No.22-1」のメッセージが出力されます。

## ディスク監視故障検知時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| 9-1	| ディスク監視 故障検知				| diskd[10935]: warning: disk status is changed, attr_name=*diskcheck_status*, target=*/dev/mapper/lun1*, new_status=ERROR	| error	| Disk connection to */dev/mapper/lun1* is ERROR. (attr_name=*diskcheck_status*)	| ディスク監視が故障を検知しました。<br>(監視対象：*/dev/mapper/lun1*)	|
- ディスク監視が"正常である"ことを検知した際には、「[属性変更時のメッセージ一覧](#属性変更時のメッセージ一覧) No.22-1」のメッセージが出力されます。

## 属性変更時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| 22-1	| 属性 更新					| (例1)<br>attrd[31167]:    info: Setting *default_ping_set*[*pm01*]: (null) -> *100* from *pm01*<br>(例2)<br>attrd[31167]:    info: Setting *diskcheck_status*[*pm01*]: (null) -> *normal* from *pm01*	| info	| (例1)<br>Attribute "*default_ping_set*" is updated to "*100*" at "*pm01*".<br>(例2)<br>Attribute "*diskcheck_status*" is updated to "*normal*" at "*pm01*".	| (例1)<br>ノード*pm01*の属性*default_ping_set*の値を *100* に更新しました。<br>→ ネットワーク監視が"正常である"ことを検知しました。<br>(例2)<br>ノード*pm01*の属性*diskcheck_status*の値を *normal* に更新しました。<br>→ ディスク監視が"正常である"ことを検知しました。	|
| 22-2	| 属性 削除					| attrd[31167]:    info: Setting *default_ping_set*[*pm01*]: *100* -> (null) from *pm01*	| info	| Attribute "*default_ping_set*" is deleted at "*pm01*".	| ノード*pm01*の属性*default_ping_set*を削除しました。	|

## STONITHリソース監視・制御時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| 17-1	| STONITHリソース起動 開始			| crmd[31169]:    info: Performing key=*50:0:0:5a50acfd-4843-4ca6-a3bc-be254cc81a6e* op=*prmStonith*_start_0	| info	| Resource *prmStonith* tries to start.			| *prmStonith*を起動(start)します。					|
| 17-2	| STONITHリソース起動 終了(成功)		| crmd[31169]:  notice: Result of start operation for *prmStonith* on *pm01*: 0 (ok)				| info	| Resource *prmStonith* started. (rc=0) ok		| *prmStonith*の起動(start)が正常に終了しました。			|
| 17-3	| STONITHリソース起動 終了(エラー)		| crmd[9816]:   error: Result of start operation for *prmStonith* on *pm01*: Error				| error	| Resource *prmStonith* failed to start. Error		| *prmStonith*の起動(start)でエラーが発生しました。			|
| 17-4	| STONITHリソース起動 終了(タイムアウト)	| crmd[16789]:   error: Result of start operation for *prmStonith* on *pm01*: Timed Out				| error	| Resource *prmStonith* failed to start. (Timed Out)	| *prmStonith*の起動(start)でタイムアウトが発生しました。		|
| 18-1	| STONITHリソース停止 開始			| crmd[31169]:    info: Performing key=*39:11:0:5a50acfd-4843-4ca6-a3bc-be254cc81a6e* op=*prmStonith*_stop_0	| info	| Resource *prmStonith* tries to stop.			| *prmStonith*を停止(stop)します。					|
| 18-2	| STONITHリソース停止 終了(成功)		| crmd[31169]:  notice: Result of stop operation for *prmStonith* on *pm01*: 0 (ok)				| info	| Resource *prmStonith* stopped. (rc=0) ok		| *prmStonith*の停止(stop)が正常に終了しました。			|
| 19-1	| STONITHリソース監視 終了(故障)		| crmd[30363]:   error: Result of monitor operation for *prmStonith* on *pm01*: Error				| error	| Resource *prmStonith* failed to monitor. Error	| *prmStonith*の監視(monitor)で故障が発生していることを検知しました。	|
| 19-3	| STONITHリソース監視 終了(タイムアウト)	| crmd[5877]:   error: Result of monitor operation for *prmStonith* on *pm01*: Timed Out			| error	| Resource *prmStonith* failed to monitor. (Timed Out)	| *prmStonith*の監視(monitor)でタイムアウトが発生しました。		|

## STONITH実行時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| 21-1	| STONITH 開始					| crmd[32598]:  notice: Requesting fencing (*reboot*) of node *pm01*									| info	| Try to STONITH (*reboot*) *pm01*.						| ノード*pm01*に対するSTONITH(*reboot*)処理を開始します。					|
| 21-2	| STONITH 終了(成功)				| crmd[32598]:  notice: Peer *pm01* was terminated (*reboot*) by *pm02* on behalf of crmd.*32598*: OK					| info	| Succeeded to STONITH (*reboot*) *pm01* by *pm02*.				| ノード*pm02*からノード*pm01*に対するSTONITH(*reboot*)処理が成功しました。			|
| 21-3	| STONITH 終了(エラー)				| crmd[17031]:  notice: Peer *pm02* was not terminated (*reboot*) by *pm01* on behalf of crmd.*17031*: *No data available*		| error	| Failed to STONITH (*reboot*) *pm02* by *pm01*.				| ノード*pm01*からノード*pm02*に対するSTONITH(*reboot*)処理が失敗しました。			|
| 21-4	| STONITH 終了(複数回エラー)			| crmd[17031]:  warning: Too many failures (*10*) to fence *pm02*, giving up								| error	| Too many failures to STONITH *pm02*.						| ノード*pm02*に対するSTONITH処理が複数回失敗しました。						|
| 21-5	| STONITH デバイス実行開始			| stonith-ng[32594]:    info: Requesting that '*pm02*' perform op '*pm01* *reboot*' with '*prmStonith*' for crmd.*32598* (*48*s)	| info	| Try to execute STONITH device *prmStonith* on *pm02* for *reboot* *pm01*.	| ノード*pm01*に対する*reboot*のため、ノード*pm02*上のSTONITHデバイス*prmStonith*を実行します。	|
| 21-6	| STONITH デバイス実行終了(成功)		| stonith-ng[32594]:  notice: Call to *prmStonith* for '*pm01* *reboot*' on behalf of crmd.*32598*@*pm02*: OK (0)			| info	| Succeeded to execute STONITH device *prmStonith* for *pm01*.			| ノード*pm01*に対するSTONITHデバイス*prmStonith*の実行が成功しました。				|
| 21-7	| STONITH デバイス実行(エラー)			| stonith-ng[32594]:  notice: Call to *prmStonith* for '*pm01* *reboot*' on behalf of crmd.*32598*@*pm02*: *No data available* (*-61*)	| warning| Failed to execute STONITH device *prmStonith* for *pm01*.			| ノード*pm01*に対するSTONITHデバイス*prmStonith*の実行が失敗しました。				|
| 21-8	| STONITH 終了(手動成功)			| crmd[17031]:  notice: Peer *pm02* was terminated (*off*) by a human on behalf of stonith_admin.*5743*: OK				| info	| Succeeded to STONITH (*off*) *pm02* by a human.				| ノード*pm02*に対する手動STONITH(*off*)処理が成功しました。					|

## フェイルオーバの開始を表すメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| F0-0	| フェイルオーバ 開始				| －	| error	| Start to fail-over.	| フェイルオーバを開始しました。	|

## フェイルオーバの完了を表すメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| F12-1	| フェイルオーバ 完了(成功)			| －	| info	| fail-over succeeded.	| フェイルオーバが成功しました。	|
| F12-2	| フェイルオーバ 完了(失敗)			| －	| error	| fail-over failed.	| フェイルオーバが失敗しました。	|

## フェイルオーバ中のリソース状態を表すメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後<br>ログの<br>priority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| :-:				| ---			| ---	|
| F11-1	| リソース 開始					| pengine[32597]:  notice: Start   *prmResource*#011(*pm02*)			| info	| Resource *prmResource* : Started on *pm02*		| *prmResource*はノード*pm02*で稼働中です。			|
| F11-2	| リソース 停止					| pengine[25227]:  notice: Stop    *prmResource*#011(*pm01*)			| error	| Resource *prmResource* : Stopped			| *prmResource*は停止しています。				|
| F11-3	| リソース 開始(配置移動なし)			| pengine[32597]:    info: Leave   *prmResource*#011(Started *pm02*)		| info	| Resource *prmResource* : Started on *pm02*		| *prmResource*はノード*pm02*で稼働中です。			|
| F11-9	| リソース 停止(配置移動なし)			| pengine[21836]:    info: Leave   *prmResource*#011(Stopped)			| error	| Resource *prmResource* : Stopped			| *prmResource*は停止しています。				|
| F11-5	| リソース Unmanaged				| pengine[4287]:    info: Leave   *prmResource*#011(Started unmanaged)		| error	| Unmanaged resource exists.				| Pacemakerが管理していない(Unmanaged)リソースがあります。	|
| F11-6	| リソース Move					| pengine[4287]:  notice: Move    *prmResource*#011(Started *pm01* -> *pm02*)	| info	| Resource *prmResource* : Move *pm01* -> *pm02*	| *prmResource*はノード*pm01*からノード*pm02*に移動します。	|
| F11-8	| リソース Restart(配置移動なし)		| pengine[25733]:  notice: Restart *prmResource*#011(Started *pm01*)		| info	| Resource *prmResource* : Started on *pm01*		| *prmResource*はノード*pm01*で稼働中です。			|
| F11-11| リソース Recover(配置移動なし)		| pengine[6419]:  notice: Recover *prmResource*#011(Started *pm01*)		| info	| Resource *prmResource* : Started on *pm01*		| *prmResource*はノード*pm01*で稼働中です。			|
| F11-12| リソース Reload(配置移動なし)			| pengine[30988]:   notice: Reload *prmResource*#011(Started *pm01*)		| info	| Resource *prmResource* : Started on *pm01*		| *prmResource*はノード*pm01*で稼働中です。			|
| F11-13| リソース Recover				| pengine[6419]:  notice: Recover *prmResource*#011(Started *pm01* -> *pm02*)	| info	| Resource *prmResource* : Move *pm01* -> *pm02*	| *prmResource*はノード*pm01*からノード*pm02*に移動します。	|
| F11-14| リソース Migrate				| pengine[6690]:  notice: Migrate *prmResource*#011(Started *pm01* -> *pm02*)	| info	| Resource *prmResource* : Move *pm01* -> *pm02*	| *prmResource*はノード*pm01*からノード*pm02*に移動します。	|

***
[Pacemakerログ解析支援ツール（pm_logconv-cs）](../README.md)
