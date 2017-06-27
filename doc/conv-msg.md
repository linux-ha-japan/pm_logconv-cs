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
- [STONITH実行時のメッセージ一覧](#stonith実行時のメッセージ一覧)
- [フェイルオーバの開始を表すメッセージ一覧](#フェイルオーバの開始を表すメッセージ一覧)
- [フェイルオーバの完了を表すメッセージ一覧](#フェイルオーバの完了を表すメッセージ一覧)
- [フェイルオーバ中のリソース状態を表すメッセージ一覧](#フェイルオーバ中のリソース状態を表すメッセージ一覧)

***
※ 表中の「**No**」は、ツール内部で使用している番号です(開発者向け)。ユーザが本番号を意識するケースはありません。

## Pacemakerサービス起動時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後ログのpriority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| ----			| ---			| ---	|
| 23-1	| サービス起動 Corosync				| corosync[31153]: [MAIN  ] Corosync Cluster Engine ('_2.4.2_'): started and ready to provide service.	| info	|Starting Corosync _2.4.2_.	| Corosync _2.4.2_ を起動します。	|
| 23-4	| サービス起動 Pacemaker			| pacemakerd[31160]:  notice: Starting Pacemaker _1.1.16-1.el7_						| info	|Starting Pacemaker _1.1.16_.	| Pacemaker _1.1.16_ を起動します。	|

## Pacemakerサービス終了時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後ログのpriority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| ----			| ---			| ---	|
| 14-1	| サービス終了 Corosync停止開始			| corosync[31154]: [SERV  ] Unloading all Corosync service engines.		| info	| Corosync is shutting down.		| Corosyncが停止処理を開始します。								|
| 14-2	| サービス終了 Corosync停止完了			| corosync[31154]: [MAIN  ] Corosync Cluster Engine exiting normally		| info	| Corosync shutdown complete.		| Corosyncの停止処理が完了しました。								|
| 14-3	| サービス終了 Pacemaker停止開始		| pacemakerd[31160]:  notice: Shutting down Pacemaker				| info	| Pacemaker is shutting down.		| Pacemakerが停止処理を開始します。								|
| 14-4	| サービス終了 Pacemaker停止完了		| pacemakerd[31160]:  notice: Shutdown complete					| info	| Pacemaker shutdown complete.		| Pacemakerの停止処理が完了しました。								|
| 14-5	| サービス終了 Pacemaker停止中			| crmd[31169]:    info: Creating shutdown request for _pm02_ (state=*S_IDLE*)	| info	| Pacemaker on _pm02_ is shutting down.	| ノード*pm02*上の、Pacemakerが停止処理を行ってます。<br>※本ログはDCノードでのみ出力されます。	|

## Pacemakerプロセス制御のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後ログのpriority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| ----			| ---			| ---	|
| 10-1	| プロセス状態 起動				| pacemakerd[31160]:    info: Forked child _31164_ for process _cib_							| info	| Start "_cib_" process. (pid=_31164_)				| *cib*プロセスが起動しました。(PID=_31164_)			|
| 10-2	| プロセス状態 異常終了(エラー発生による終了①)	| pacemakerd[24012]:   error: The _crmd_ process (_24021_) exited: _Generic Pacemaker error_ (_201_)			| warning| Managed "_crmd_" process exited. (pid=_24021_, rc=_201_)	| *crmd*プロセス(PID=_24021_)が終了コード*201*で終了しました。	|
| 10-4	| プロセス状態 異常終了(エラー発生による終了②)	| pacemakerd[16364]: warning: The _crmd_ process (_16373_) can no longer be respawned, shutting the cluster down.	| warning| Managed "_crmd_" process exited. (pid=_16373_, rc=_100_)	| *crmd*プロセス(PID=_16373_)が、終了コード*100*で終了しました。|
| 10-5	| プロセス状態 異常終了(エラー発生による終了③)	| pacemakerd[8627]:   emerg: The _crmd_ process (_8635_) instructed the machine to reset				| warning| Managed "_crmd_" process exited. (pid=_8635_, rc=_255_)	| *crmd*プロセス(PID=_8635_)が、終了コード*255*で終了しました。	|
| 10-3	| プロセス状態 異常終了(シグナルによる終了)	| (1. SIGKILLによる終了)<br>pacemakerd[24012]: warning: The _cib_ process (_24016_) terminated with signal _9_ (core=_0_)<br>(2. SIGKILL以外のシグナルによる終了)<br>pacemakerd[9746]:   error: The _cib_ process (_9750_) terminated with signal _1_ (core=_0_)	| warning| (1)<br>Managed "_cib_" process terminated with signal _9_. (pid=_24016_)<br>(2)<br>Managed "_cib_" process terminated with signal _1_. (pid=_9750_)	| (1)<br>*cib*プロセス(PID=_24016_)がシグナル*9*番によって停止しました。<br>(2)<br>*cib*プロセス(PID=_9750_)がシグナル*1*番によって停止しました。	|
| 10-6	| プロセス状態 正常終了				| pacemakerd[31160]:    info: The _cib_ process (_31164_) exited: OK (0)						| info	| Stop "_cib_" process normally. (pid=_31164_)			| *cib*プロセス(PID=_31164_)が正常に終了しました。		|
| 10-7	| プロセス状態 複数回異常終了			| pacemakerd[30354]:   error: Child respawn count exceeded by _stonith-ng_						| error	| Respawn count exceeded by "_stonith-ng_".			| *stonith-ng*プロセスが再起動回数を超過しました。		|

## ノード状態変更時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後ログのpriority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| ----			| ---			| ---	|
| 6-1	| ノード状態 離脱				| crmd[1404]:    info: Cluster node _pm01_ is now lost (was member)									| warning| Node _pm01_ is lost	| ノード*pm01*がクラスタメンバシップから離脱しました。	|
| 6-2	| ノード状態 参加				| crmd[8623]:    info: _pm01_ is now member<br>または<br>crmd[31169]:    info: Cluster node _pm01_ is now member (was in unknown state)	| info	| Node _pm01_ is member	| ノード*pm01*がクラスタメンバシップに参加しました。	|

## DC遷移時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後ログのpriority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| ----			| ---			| ---	|
| 13-2	| DC遷移 選出					| crmd[31169]:    info: Set DC to _pm01_ (_3.0.11_)	| info	| Set DC node to _pm01_.	| ノード*pm01*がDCノードに選出されました。	|
| 13-5	| DC遷移 剥奪					| crmd[8623]:    info: Unset DC. Was _pm01_		| info	| Unset DC node _pm01_.		| ノード*pm01*がDCノードではなくなりました。	|

## リソース監視・制御時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後ログのpriority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| ----			| ---			| ---	|
| 1-1	| リソース起動 開始				| crmd[31169]:    info: Performing key=_36:0:0:5a50acfd-4843-4ca6-a3bc-be254cc81a6e_ op=_prmResource_\_start\_0		| info	| Resource _prmResource_ tries to start.				| *prmResource*を起動(start)します。						|
| 1-2	| リソース起動 終了(成功)			| crmd[31169]:  notice: Result of start operation for _prmResource_ on _pm01_: 0 (ok)					| info	| Resource _prmResource_ started. (rc=0) ok				| *prmResource*の起動(start)が正常に終了しました。				|
| 1-3	| リソース起動 終了(エラー)			| crmd[18806]:  notice: Result of start operation for _prmResource_ on _pm01_: _1_ (_unknown error_)			| error	| Resource _prmResource_ failed to start. (rc=_1_) _unknown error_	| *prmResource*の起動(start)でエラーが発生しました。				|
| 1-4	| リソース起動 終了(タイムアウト)		| crmd[32231]:   error: Result of start operation for _prmResource_ on _pm01_: Timed Out				| error	| Resource _prmResource_ failed to start. (Timed Out)			| *prmResource*の起動(start)でタイムアウトが発生しました。			|
| 2-1	| リソース停止 開始				| crmd[31169]:    info: Performing key=_19:11:0:5a50acfd-4843-4ca6-a3bc-be254cc81a6e_ op=_prmResource_\_stop\_0		| info	| Resource _prmResource_ tries to stop.					| *prmResource*を停止(stop)します。						|
| 2-2	| リソース停止 終了(成功)			| crmd[31169]:  notice: Result of stop operation for _prmResource_ on _pm01_: 0 (ok)					| info	| Resource _prmResource_ stopped. (rc=0) ok				| *prmResource*の停止(stop)が正常に終了しました。				|
| 2-3	| リソース停止 終了(エラー)			| crmd[9457]:  notice: Result of stop operation for _prmResource_ on _pm01_: _1_ (_unknown error_)			| error	| Resource _prmResource_ failed to stop. (rc=_1_) _unknown error_	| *prmResource*の停止(stop)でエラーが発生しました。				|
| 2-4	| リソース停止 終了(タイムアウト)		| crmd[6529]:   error: Result of stop operation for _prmResource_ on _pm01_: Timed Out					| error	| Resource _prmResource_ failed to stop. (Timed Out)			| *prmResource*の停止(stop)でタイムアウトが発生しました。			|
| 3-1	| リソース監視 終了(エラー)			| crmd[6475]:    info: Result of monitor operation for _prmResource_ on _pm01_: _1_ (_unknown error_)			| error	| Resource _prmResource_ failed to monitor. (rc=_1_) _unknown error_	| *prmResource*の監視(monitor)で故障が発生していることを検知しました。		|
| 3-2	| リソース監視 終了(停止検知)			| crmd[6387]:    info: Result of monitor operation for _prmResource_ on _pm01_: 7 (not running)				| error	| Resource _prmResource_ does not work. (rc=7) not running		| *prmResource*の監視(monitor)でリソースが停止していることを検知しました。	|
| 3-3	| リソース監視 終了(タイムアウト)		| crmd[14390]:   error: Result of monitor operation for _prmResource_ on _pm01_: Timed Out				| error	| Resource _prmResource_ failed to monitor. (Timed Out)			| *prmResource*の監視(monitor)でタイムアウトが発生しました。			|
| 4-1	| リソースMaster化 開始				| crmd[31169]:    info: Performing key=_39:6:0:5a50acfd-4843-4ca6-a3bc-be254cc81a6e_ op=_prmResource_\_promote\_0	| info	| Resource _prmResource_ tries to promote.				| *prmResource*をMaster化(promote)します。					|
| 4-2	| リソースMaster化 終了(成功)			| crmd[31169]:  notice: Result of promote operation for _prmResource_ on _pm01_: 0 (ok)					| info	| Resource _prmResource_ promoted. (rc=0) ok				| *prmResource*のMaster化(promote)が正常に終了しました。			|
| 4-3	| リソースMaster化 終了(エラー)			| crmd[25809]:  notice: Result of promote operation for _prmResource_ on _pm01_: _1_ (_unknown error_)			| error	| Resource _prmResource_ failed to promote. (rc=_1_) _unknown error_	| *prmResource*のMaster化(promote)でエラーが発生しました。			|
| 4-4	| リソースMaster化 終了(タイムアウト)		| crmd[32042]:   error: Result of promote operation for _prmResource_ on _pm01_: Timed Out				| error	| Resource _prmResource_ failed to promote. (Timed Out)			| *prmResource*のMaster化(promote)でタイムアウトが発生しました。		|
| 5-1	| リソースSlave化 開始				| crmd[31169]:    info: Performing key=_44:11:0:5a50acfd-4843-4ca6-a3bc-be254cc81a6e_ op=_prmResource_\_demote\_0	| info	| Resource _prmResource_ tries to demote.				| *prmResource*をSlave化(demote)します。					|
| 5-2	| リソースSlave化 終了(成功)			| crmd[31169]:  notice: Result of demote operation for _prmResource_ on _pm01_: 0 (ok)					| info	| Resource _prmResource_ demoted. (rc=0) ok				| *prmResource*のSlave化(demote)が正常に終了しました。				|
| 5-3	| リソースSlave化 終了(エラー)			| crmd[6118]:  notice: Result of demote operation for _prmResource_ on _pm01_: _1_ (_unknown error_)			| error	| Resource _prmResource_ failed to demote. (rc=_1_) _unknown error_	| *prmResource*のSlave化(demote)でエラーが発生しました。			|
| 5-4	| リソースSlave化 終了(タイムアウト)		| crmd[6336]:   error: Result of demote operation for _prmResource_ on _pm01_: Timed Out				| error	| Resource _prmResource_ failed to demote. (Timed Out)			| *prmResource*のSlave化(demote)でタイムアウトが発生しました。			|

## リソース移行時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後ログのpriority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| ----			| ---			| ---	|
| 11-1	| リソース移行(migrate_to) 開始			| crmd[6691]:    info: Performing key=_22:12:0:e13dcf24-6449-46a2-acbe-c69187f41539_ op=_prmResource_\_migrate\_to\_0		| info	| Resource _prmResource_ tries to migrate_to.					| *prmResource*を移行(migrate_to)します。				|
| 11-2	| リソース移行(migrate_to) 終了(成功)		| crmd[6691]:  notice: Result of migrate_to operation for _prmResource_ on _pm01_: 0 (ok)					| info	| Resource _prmResource_ migrated_to. (rc=0) ok					| *prmResource*の移行(migrate_to)が正常に終了しました。			|
| 11-3	| リソース移行(migrate_to) 終了(エラー)		| crmd[13234]:  notice: Result of migrate_to operation for _prmResource_ on _pm01_: _1_ (_unknown error_)			| error	| Resource _prmResource_ failed to migrate_to. (rc=_1_) _unknown error_		| *prmResource*の移行(migrate_to)でエラーが発生しました。		|
| 11-4	| リソース移行(migrate_to) 終了(タイムアウト)	| crmd[19780]:   error: Result of migrate_to operation for _prmResource_ on _pm01_: Timed Out					| error	| Resource _prmResource_ failed to migrate_to. (Timed Out)			| *prmResource*の移行(migrate_to)でタイムアウトが発生しました。		|
| 12-1	| リソース移行(migrate_from) 開始		| crmd[14239]:    info: Performing key=_23:12:0:e13dcf24-6449-46a2-acbe-c69187f41539_ op=_prmResource_\_migrate\_from\_0	| info	| Resource _prmResource_ tries to migrate_from.					| *prmResource*を移行(migrate_from)します。				|
| 12-2	| リソース移行(migrate_from) 終了(成功)		| crmd[14239]:  notice: Result of migrate_from operation for _prmResource_ on _pm01_: 0 (ok)					| info	| Resource _prmResource_ migrated_from. (rc=0) ok				| *prmResource*の移行(migrate_from)が正常に終了しました。		|
| 12-3	| リソース移行(migrate_from) 終了(エラー)	| crmd[24474]:  notice: Result of migrate_from operation for _prmResource_ on _pm01_: _1_ (_unknown error_)			| error	| Resource _prmResource_ failed to migrate_from. (rc=_1_) _unknown error_	| *prmResource*の移行(migrate_from)でエラーが発生しました。		|
| 12-4	| リソース移行(migrate_from) 終了(タイムアウト)	| crmd[29987]:   error: Result of migrate_from operation for _prmResource_ on _pm01_: Timed Out					| error	| Resource _prmResource_ failed to migrate_from. (Timed Out)			| *prmResource*の移行(migrate_from)でタイムアウトが発生しました。	|

## インターコネクトLAN状態変更時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後ログのpriority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| ----			| ---			| ---	|
| 7-1	| インターコネクトLAN状態 故障検知		| corosync[25418]: [TOTEM ] Marking seqid _11906_ ringid _0_ interface _192.168.101.1_ FAULTY	| warning| Ring number _0_ is FAULTY (interface _192.168.101.1_).	| インターコネクトLAN _192.168.101.1_ (リングナンバー _0_)の故障/停止を検知しました。	|
| 7-2	| インターコネクトLAN状態 回復検知		| corosync[25418]: [TOTEM ] Automatically recovered ring _0_					| info	| Ring number _0_ is recovered.					| インターコネクトLAN(リングナンバー _0_)の回復を検知しました。				|

## ネットワーク監視故障検知時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後ログのpriority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| ----			| ---			| ---	|
| 8-1	| ネットワーク監視 故障検知			| ping(_prmPing_)[13509]: WARNING: _192.168.201.254_ is inactive: PING _192.168.201.254_ (_192.168.201.254_) 56(84) bytes of data.#012#012--- _192.168.201.254_ ping statistics ---#0122 packets transmitted, 0 received, 100% packet loss, time *1005*ms	| error	| Network to _192.168.201.254_ is unreachable.	| ネットワーク監視が故障を検知しました。<br>(監視先IPアドレス _192.168.201.254_ に対して通信できませんでした)	|
- ネットワーク監視が"正常である"ことを検知した際には、「[属性変更時のメッセージ一覧](#属性変更時のメッセージ一覧) No.22-1」のメッセージが出力されます。

## ディスク監視故障検知時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後ログのpriority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| ----			| ---			| ---	|
| 9-1	| ディスク監視 故障検知				| diskd[10935]: warning: disk status is changed, attr_name=_diskcheck_status_, target=_/dev/mapper/lun1_, new_status=ERROR	| error	| Disk connection to _/dev/mapper/lun1_ is ERROR. (attr_name=_diskcheck_status_)	| ディスク監視が故障を検知しました。<br>(監視対象：_/dev/mapper/lun1_)	|
- ディスク監視が"正常である"ことを検知した際には、「[属性変更時のメッセージ一覧](#属性変更時のメッセージ一覧) No.22-1」のメッセージが出力されます。

## 属性変更時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後ログのpriority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| ----			| ---			| ---	|
| 22-1	| 属性 更新					| (例1)<br>attrd[31167]:    info: Setting _default_ping_set_[_pm01_]: (null) -> _100_ from _pm01_<br>(例2)<br>attrd[31167]:    info: Setting _diskcheck_status_[_pm01_]: (null) -> _normal_ from _pm01_	| info	| (例1)<br>Attribute "_default_ping_set_" is updated to "_100_" at "_pm01_".<br>(例2)<br>Attribute "_diskcheck_status_" is updated to "_normal_" at "_pm01_".	| (例1)<br>ノード*pm01*の属性*default_ping_set*の値を _100_ に更新しました。<br>→ ネットワーク監視が"正常である"ことを検知しました。<br>(例2)<br>ノード*pm01*の属性*diskcheck_status*の値を _normal_ に更新しました。<br>→ ディスク監視が"正常である"ことを検知しました。	|
| 22-2	| 属性 削除					| attrd[31167]:    info: Setting _default_ping_set_[_pm01_]: _100_ -> (null) from _pm01_	| info	| Attribute "_default_ping_set_" is deleted at "_pm01_".	| ノード*pm01*の属性*default_ping_set*を削除しました。	|

## STONITH実行時のメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後ログのpriority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| ----			| ---			| ---	|
| 21-1	| STONITH 開始					| crmd[32598]:  notice: Requesting fencing (_reboot_) of node _pm01_														| info	| Try to STONITH (_reboot_) _pm01_.						| ノード*pm01*に対するSTONITH(_reboot_)処理を開始します。					|
| 21-2	| STONITH 終了(成功)				| crmd[32598]:  notice: Peer _pm01_ was terminated (_reboot_) by _pm02_ for _pm02_: OK (ref=_930847f8-9484-4339-a13a-59239a029c2d_) by client crmd._32598_			| info	| Succeeded to STONITH (_reboot_) _pm01_ by _pm02_.				| ノード*pm02*からノード*pm01*に対するSTONITH(_reboot_)処理が成功しました。			|
| 21-3	| STONITH 終了(エラー)				| crmd[17031]:  notice: Peer _pm02_ was not terminated (_reboot_) by _pm01_ for _pm01_: _No data available_ (ref=_1165e1c6-a647-47c4-844a-ec7375a54ac8_) by client crmd._17031_	| error	| Failed to STONITH (_reboot_) _pm02_ by _pm01_.				| ノード*pm01*からノード*pm02*に対するSTONITH(_reboot_)処理が失敗しました。			|
| 21-4	| STONITH 終了(複数回エラー)			| crmd[17031]:  notice: Too many failures to fence _pm02_ (_11_), giving up													| error	| Too many failures to STONITH _pm02_.						| ノード*pm02*に対するSTONITH処理が複数回失敗しました。						|
| 21-5	| STONITH デバイス実行開始			| stonith-ng[32594]:    info: Requesting that '_pm02_' perform op '_pm01_ _reboot_' with '_prmStonith_' for crmd._32598_ (*48*s)						| info	| Try to execute STONITH device _prmStonith_ on _pm02_ for _reboot_ _pm01_.	| ノード*pm01*に対する*reboot*のため、ノード*pm02*上のSTONITHデバイス*prmStonith*を実行します。	|
| 21-6	| STONITH デバイス実行終了(成功)		| stonith-ng[32594]:  notice: Call to _prmStonith_ for '_pm01_ _reboot_' on behalf of crmd._32598_@_pm02_: OK (0)								| info	| Succeeded to execute STONITH device _prmStonith_ for _pm01_.			| ノード*pm01*に対するSTONITHデバイス*prmStonith*の実行が成功しました。				|
| 21-7	| STONITH デバイス実行(エラー)			| stonith-ng[32594]:  notice: Call to _prmStonith_ for '_pm01_ _reboot_' on behalf of crmd._32598_@_pm02_: _No data available_ (_-61_)						| warning| Failed to execute STONITH device _prmStonith_ for _pm01_.			| ノード*pm01*に対するSTONITHデバイス*prmStonith*の実行が失敗しました。				|
| 21-8	| STONITH 終了(手動成功)			| crmd[17031]:  notice: Peer _pm02_ was terminated (_off_) by a human for _pm01_: OK (ref=_882ab3f0-28a7-4d70-9a2b-8ce9b76a2235_) by client stonith_admin._5743_		| info	| Succeeded to STONITH (_off_) _pm02_ by a human.				| ノード*pm02*に対する手動STONITH(_off_)処理が成功しました。					|

## フェイルオーバの開始を表すメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後ログのpriority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| ----			| ---			| ---	|
| F0-0	| フェイルオーバ 開始				| －	| error	| Start to fail-over.	| フェイルオーバを開始しました。	|

## フェイルオーバの完了を表すメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後ログのpriority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| ----			| ---			| ---	|
| F12-1	| フェイルオーバ 完了(成功)			| －	| info	| fail-over succeeded.	| フェイルオーバが成功しました。	|
| F12-2	| フェイルオーバ 完了(失敗)			| －	| error	| fail-over failed.	| フェイルオーバが失敗しました。	|

## フェイルオーバ中のリソース状態を表すメッセージ一覧
| No	| イベント	| Pacemakerログの例	| 変換後ログのpriority	| 変換後ログメッセージ	| 意味	|
| ---	| ---		| ---			| ----			| ---			| ---	|
| F11-1	| リソース 開始					| pengine[32597]:  notice: Start   _prmResource_#011(_pm02_)			| info	| Resource _prmResource_ : Started on _pm02_		| *prmResource*はノード*pm02*で稼働中です。			|
| F11-2	| リソース 停止					| pengine[25227]:  notice: Stop    _prmResource_#011(_pm01_)			| error	| Resource _prmResource_ : Stopped			| *prmResource*は停止しています。				|
| F11-3	| リソース 開始(配置移動なし)			| pengine[32597]:    info: Leave   _prmResource_#011(Started _pm02_)		| info	| Resource _prmResource_ : Started on _pm02_		| *prmResource*はノード*pm02*で稼働中です。			|
| F11-9	| リソース 停止(配置移動なし)			| pengine[21836]:    info: Leave   _prmResource_#011(Stopped)			| error	| Resource _prmResource_ : Stopped			| *prmResource*は停止しています。				|
| F11-5	| リソース Unmanaged				| pengine[4287]:    info: Leave   _prmResource_#011(Started unmanaged)		| error	| Unmanaged resource exists.				| Pacemakerが管理していない(Unmanaged)リソースがあります。	|
| F11-6	| リソース Move					| pengine[4287]:  notice: Move    _prmResource_#011(Started _pm01_ -> _pm02_)	| info	| Resource _prmResource_ : Move _pm01_ -> _pm02_	| *prmResource*はノード*pm01*からノード*pm02*に移動します。	|
| F11-8	| リソース Restart(配置移動なし)		| pengine[25733]:  notice: Restart _prmResource_#011(Started _pm01_)		| info	| Resource _prmResource_ : Started on _pm01_		| *prmResource*はノード*pm01*で稼働中です。			|
| F11-11| リソース Recover(配置移動なし)		| pengine[6419]:  notice: Recover _prmResource_#011(Started _pm01_)		| info	| Resource _prmResource_ : Started on _pm01_		| *prmResource*はノード*pm01*で稼働中です。			|
| F11-12| リソース Reload(配置移動なし)			| pengine[30988]:   notice: Reload _prmResource_#011(Started _pm01_)		| info	| Resource _prmResource_ : Started on _pm01_		| *prmResource*はノード*pm01*で稼働中です。			|
| F11-13| リソース Recover				| pengine[6419]:  notice: Recover _prmResource_#011(Started _pm01_ -> _pm02_)	| info	| Resource _prmResource_ : Move _pm01_ -> _pm02_	| *prmResource*はノード*pm01*からノード*pm02*に移動します。	|
| F11-14| リソース Migrate				| pengine[6690]:  notice: Migrate _prmResource_#011(Started _pm01_ -> _pm02_)	| info	| Resource _prmResource_ : Move _pm01_ -> _pm02_	| *prmResource*はノード*pm01*からノード*pm02*に移動します。	|

***
[Pacemakerログ解析支援ツール（pm_logconv-cs）](../README.md)
