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
- [STONITHリソース制御時のメッセージ一覧](#stonithリソース制御時のメッセージ一覧)
- [STONITH実行時のメッセージ一覧](#stonith実行時のメッセージ一覧)
- [フェイルオーバの開始を表すメッセージ一覧](#フェイルオーバの開始を表すメッセージ一覧)
- [フェイルオーバの完了を表すメッセージ一覧](#フェイルオーバの完了を表すメッセージ一覧)
- [フェイルオーバ中のリソース状態を表すメッセージ一覧](#フェイルオーバ中のリソース状態を表すメッセージ一覧)

## Pacemakerサービス起動時のメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| 23-1	| サービス起動 Corosync				| info	|Starting Corosync _2.4.2_.	| Corosync _2.4.2_ を起動します。	|
| 23-4	| サービス起動 Pacemaker			| info	|Starting Pacemaker _1.1.16_.	| Pacemaker _1.1.16_ を起動します。	|

## Pacemakerサービス終了時のメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| 14-1	| サービス終了 Corosync停止開始			| info	| Corosync is shutting down.		| Corosyncが停止処理を開始します。									|
| 14-2	| サービス終了 Corosync停止完了			| info	| Corosync shutdown complete.		| Corosyncの停止処理が完了しました。									|
| 14-3	| サービス終了 Pacemaker停止開始		| info	| Pacemaker is shutting down.		| Pacemakerが停止処理を開始します。									|
| 14-4	| サービス終了 Pacemaker停止完了		| info	| Pacemaker shutdown complete.		| Pacemakerの停止処理が完了しました。									|
| 14-5	| サービス終了 Pacemaker停止中			| info	| Pacemaker on _pm02_ is shutting down.	| ノード"_pm02_"上の、Pacemakerが停止処理を行ってます。<br>※本ログはDCノードでのみ出力されます。	|

## Pacemakerプロセス制御のメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| 10-1	| プロセス状態 起動				| info	| Start "_cib_" process. (pid=_888_)					| _cib_ プロセスが起動しました。(PID=_888_)				|
| 10-2	| プロセス状態 異常終了(エラー発生による終了)	| warning| Managed "_crmd_" process exited. (pid=_2964_, rc=_201_)		| _crmd_ プロセス(PID=_2964_)が終了コード*201*で終了しました。		|
| 10-3	| プロセス状態 異常終了(シグナルによる終了)	| warning| Managed "_cib_" process terminated with signal _9_. (pid=_1693_)	| _cib_ プロセス(PID=_1693_)がシグナル*9*番によって停止しました。	|
| 10-6	| プロセス状態 正常終了				| info	| Stop "_cib_" process normally. (pid=_1693_)				| _cib_ プロセス(PID=_1693_)が正常に終了しました。			|
| 10-7	| プロセス状態 複数回異常終了			| error	| Respawn count exceeded by "_cib_".					| _cib_ プロセスが再起動回数を超過しました。				|

## ノード状態変更時のメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| 6-1	| ノード状態 離脱				| warning| Node _pm02_ is lost	| ノード"_pm02_"がクラスタメンバシップから離脱しました。	|
| 6-2	| ノード状態 参加				| info	| Node _pm02_ is member	| ノード"_pm02_"がクラスタメンバシップに参加しました。		|

## DC遷移時のメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| 13-2	| DC遷移 選出					| info	| Set DC node to _pm01_.	| ノード"_pm01_"がDCノードに選出されました。	|
| 13-5	| DC遷移 剥奪					| info	| Unset DC node _pm02_.		| ノード"_pm02_"がDCノードではなくなりました。	|

## リソース監視・制御時のメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| 1-1	| リソース起動 開始				| info	| Resource _prmResource_ tries to start.				| リソースID"_prmResource_"を起動(start)します。					|
| 1-2	| リソース起動 終了(成功)			| info	| Resource _prmResource_ started. (rc=0) ok				| リソースID"_prmResource_"の起動(start)が正常に終了しました。				|
| 1-3	| リソース起動 終了(エラー)			| error	| Resource _prmResource_ failed to start. (rc=_1_) _unknown error_	| リソースID"_prmResource_"の起動(start)でエラーが発生しました。			|
| 1-4	| リソース起動 終了(タイムアウト)		| error	| Resource _prmResource_ failed to start. (Timed Out)			| リソースID"_prmResource_"の起動(start)でタイムアウトが発生しました。			|
| 2-1	| リソース停止 開始				| info	| Resource _prmResource_ tries to stop.					| リソースID"_prmResource_"を停止(stop)します。						|
| 2-2	| リソース停止 終了(成功)			| info	| Resource _prmResource_ stopped. (rc=0) ok				| リソースID"_prmResource_"の停止(stop)が正常に終了しました。				|
| 2-3	| リソース停止 終了(エラー)			| error	| Resource _prmResource_ failed to stop. (rc=_1_) _unknown error_	| リソースID"_prmResource_"の停止(stop)でエラーが発生しました。				|
| 2-4	| リソース停止 終了(タイムアウト)		| error	| Resource _prmResource_ failed to stop. (Timed Out)			| リソースID"_prmResource_"の停止(stop)でタイムアウトが発生しました。			|
| 3-1	| リソース監視 終了(エラー)			| error	| Resource _prmResource_ failed to monitor. (rc=_1_) _unknown error_	| リソースID"_prmResource_"の監視(monitor)で故障が発生していることを検知しました。	|
| 3-2	| リソース監視 終了(停止検知)			| error	| Resource _prmResource_ does not work. (rc=7) not running		| リソースID"_prmResource_"の監視(monitor)でリソースが停止していることを検知しました。	|
| 3-3	| リソース監視 終了(タイムアウト)		| error	| Resource _prmResource_ failed to monitor. (Timed Out)			| リソースID"_prmResource_"の監視(monitor)でタイムアウトが発生しました。		|
| 4-1	| リソースMaster化 開始				| info	| Resource _prmResource_ tries to promote.				| リソースID"_prmResource_"をMaster化(promote)します。					|
| 4-2	| リソースMaster化 終了(成功)			| info	| Resource _prmResource_ promoted. (rc=0) ok				| リソースID"_prmResource_"のMaster化(promote)が正常に終了しました。			|
| 4-3	| リソースMaster化 終了(エラー)			| error	| Resource _prmResource_ failed to promote. (rc=_1_) _unknown error_	| リソースID"_prmResource_"のMaster化(promote)でエラーが発生しました。			|
| 4-4	| リソースMaster化 終了(タイムアウト)		| error	| Resource _prmResource_ failed to promote. (Timed Out)			| リソースID"_prmResource_"のMaster化(promote)でタイムアウトが発生しました。		|
| 5-1	| リソースSlave化 開始				| info	| Resource _prmResource_ tries to demote.				| リソースID"_prmResource_"をSlave化(demote)します。					|
| 5-2	| リソースSlave化 終了(成功)			| info	| Resource _prmResource_ demoted. (rc=0) ok				| リソースID"_prmResource_"のSlave化(demote)が正常に終了しました。			|
| 5-3	| リソースSlave化 終了(エラー)			| error	| Resource _prmResource_ failed to demote. (rc=_1_) _unknown error_	| リソースID"_prmResource_"のSlave化(demote)でエラーが発生しました。			|
| 5-4	| リソースSlave化 終了(タイムアウト)		| error	| Resource _prmResource_ failed to demote. (Timed Out)			| リソースID"_prmResource_"のSlave化(demote)でタイムアウトが発生しました。		|

## リソース移行時のメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| 11-1	| リソース移行(migrate_to) 開始			| info	| Resource _prmResource_ tries to migrate_to.					| リソースID"_prmResource_"を移行(migrate_to)します。				|
| 11-2	| リソース移行(migrate_to) 終了(成功)		| info	| Resource _prmResource_ migrated_to. (rc=0) ok					| リソースID"_prmResource_"の移行(migrate_to)が正常に終了しました。		|
| 11-3	| リソース移行(migrate_to) 終了(エラー)		| error	| Resource _prmResource_ failed to migrate_to. (rc=_1_) _unknown error_		| リソースID"_prmResource_"の移行(migrate_to)でエラーが発生しました。		|
| 11-4	| リソース移行(migrate_to) 終了(タイムアウト)	| error	| Resource _prmResource_ failed to migrate_to. (Timed Out)			| リソースID"_prmResource_"の移行(migrate_to)でタイムアウトが発生しました。	|
| 12-1	| リソース移行(migrate_from) 開始		| info	| Resource _prmResource_ tries to migrate_from.					| リソースID"_prmResource_"を移行(migrate_from)します。				|
| 12-2	| リソース移行(migrate_from) 終了(成功)		| info	| Resource _prmResource_ migrated_from. (rc=0) ok				| リソースID"_prmResource_"の移行(migrate_from)が正常に終了しました。		|
| 12-3	| リソース移行(migrate_from) 終了(エラー)	| error	| Resource _prmResource_ failed to migrate_from. (rc=_1_) _unknown error_	| リソースID"_prmResource_"の移行(migrate_from)でエラーが発生しました。		|
| 12-4	| リソース移行(migrate_from) 終了(タイムアウト)	| error	| Resource _prmResource_ failed to migrate_from. (Timed Out)			| リソースID"_prmResource_"の移行(migrate_from)でタイムアウトが発生しました。	|

## インターコネクトLAN状態変更時のメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| 7-1	| インターコネクトLAN状態 故障検知		| warning| Ring number _0_ is FAULTY (interface _192.168.101.1_).	| インターコネクトLAN"_192.168.101.1_"(リングナンバー"_0_")の故障/停止を検知しました。	|
| 7-2	| インターコネクトLAN状態 回復検知		| info	| Ring number _0_ is recovered.					| インターコネクトLAN(リングナンバー"_0_")の回復を検知しました。			|

## ネットワーク監視故障検知時のメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| 8-1	| ネットワーク監視 故障検知			| error	| Network to _192.168.201.254_ is unreachable.	| ネットワーク監視が故障を検知しました。<br>(監視先IPアドレス"_192.168.201.254_"に対して通信できませんでした)	|
- ネットワーク監視が"正常である"ことを検知した際には、「[属性変更時のメッセージ一覧](#属性変更時のメッセージ一覧) No.22-1」のメッセージが出力されます。

## ディスク監視故障検知時のメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| 9-1	| ディスク監視 故障検知				| error	| Disk connection to _/dev/mapper/lun1_ is ERROR. (attr_name=_diskcheck_status_)	| ディスク監視が故障を検知しました。<br>(監視対象：_/dev/mapper/lun1_)	|
- ディスク監視が"正常である"ことを検知した際には、「[属性変更時のメッセージ一覧](#属性変更時のメッセージ一覧) No.22-1」のメッセージが出力されます。

## 属性変更時のメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| 22-1	| 属性 更新					| info	| (例1)<br>Attribute "_default_ping_set_" is updated to "_100_" at "_pm01_".<br><br>(例2)<br>Attribute "_diskcheck_status_" is updated to "normal" at "_pm01_".	| (例1)<br>ノード"_pm01_"の属性"_default_ping_set_"の値を"_100_"に更新しました。<br>→ ネットワーク監視が"正常である"ことを検知しました。<br>(例2)<br>ノード"_pm01_"の属性"_diskcheck_status_"の値を"normal"に更新しました。<br>→ ディスク監視が"正常である"ことを検知しました。	|
| 22-2	| 属性 削除					| info	| Attribute "_default_ping_set_" is deleted at "_pm01_".	| ノード"_pm01_"の属性"_default_ping_set_"を削除しました。	|

## STONITHリソース制御時のメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| 17-1	| STONITHリソース起動 開始			| info	| Resource _prmStonith_ tries to start.			| リソースID"_prmStonith_"を起動(start)します。						|
| 17-2	| STONITHリソース起動 終了(成功)		| info	| Resource _prmStonith_ started. (rc=0) ok		| リソースID"_prmStonith_"の起動(start)が正常に終了しました。				|
| 17-3	| STONITHリソース起動 終了(エラー)		| error	| Resource _prmStonith_ failed to start. _Error_	| リソースID"_prmStonith_"の起動(start)でエラーが発生しました。				|
| 17-4	| STONITHリソース起動 終了(タイムアウト)	| error	| Resource _prmStonith_ failed to start. (Timed Out)	| リソースID"_prmStonith_"の起動(start)でタイムアウトが発生しました。			|
| 18-1	| STONITHリソース停止 開始			| info	| Resource _prmStonith_ tries to stop.			| リソースID"_prmStonith_"を停止(stop)します。						|
| 18-2	| STONITHリソース停止 終了(成功)		| info	| Resource _prmStonith_ stopped. (rc=0) ok		| リソースID"_prmStonith_"の停止(stop)が正常に終了しました。				|
| 19-1	| STONITHリソース監視 終了(故障)		| error	| Resource _prmStonith_ failed to monitor. _Error_	| リソースID"_prmStonith_"の監視(monitor)で故障が発生していることを検知しました。	|
| 19-3	| STONITHリソース監視 終了(タイムアウト)	| error	| Resource _prmStonith_ failed to monitor. (Timed Out)	| リソースID"_prmStonith_"の監視(monitor)でタイムアウトが発生しました。			|

## STONITH実行時のメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| 21-1	| STONITH 開始					| info	| Try to STONITH (_reboot_) _pm02_.						| ノード"_pm02_"に対するSTONITH(_reboot_)処理を開始します。						|
| 21-2	| STONITH 終了(成功)				| info	| Succeeded to STONITH (_reboot_) _pm02_ by _pm01_.				| ノード"_pm01_"からノード"_pm02_"に対するSTONITH(_reboot_)処理が成功しました。				|
| 21-3	| STONITH 終了(エラー)				| error	| Failed to STONITH (_reboot_) _pm02_ by _pm01_.				| ノード"_pm01_"からノード"_pm02_"に対するSTONITH(_reboot_)処理が失敗しました。				|
| 21-4	| STONITH 終了(複数回エラー)			| error	| Too many failures to STONITH _pm02_.						| ノード"_pm02_"に対するSTONITH処理が複数回失敗しました。						|
| 21-5	| STONITH デバイス実行開始			| info	| Try to execute STONITH device _prmStonith_ on _pm01_ for _reboot_ _pm02_.	| ノード"_pm02_"に対する*reboot*のため、ノード"_pm01_"上のSTONITHデバイス"_prmStonith_"を実行します。	|
| 21-6	| STONITH デバイス実行終了(成功)		| info	| Succeeded to execute STONITH device _prmStonith_ for _pm02_.			| ノード"_pm02_"に対するSTONITHデバイス"_prmStonith_"の実行が成功しました。				|
| 21-7	| STONITH デバイス実行(エラー)			| warning| Failed to execute STONITH device _prmStonith_ for _pm02_.			| ノード"_pm02_"に対するSTONITHデバイス"_prmStonith_"の実行が失敗しました。				|
| 21-8	| STONITH 終了(手動成功)			| info	| Succeeded to STONITH (_off_) _pm02_ by a human.				| ノード"_pm02_"に対する手動STONITH(_off_)処理が成功しました。						|

## フェイルオーバの開始を表すメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| F0-0	| フェイルオーバ 開始				| error	| Start to fail-over.	| フェイルオーバを開始しました。	|

## フェイルオーバの完了を表すメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| F12-1	| フェイルオーバ 完了(成功)			| info	| fail-over succeeded.	| フェイルオーバが成功しました。	|
| F12-2	| フェイルオーバ 完了(失敗)			| error	| fail-over failed.	| フェイルオーバが失敗しました。	|

## フェイルオーバ中のリソース状態を表すメッセージ一覧
| No	| イベント	| priority	| メッセージ	| 意味	|
| -	| -		| -		| -		| -	|
| F11-1	| リソース 開始					| info	| Resource _prmResource_ : Started on _pm01_		| リソースID"_prmResource_"はノード"_pm01_"で稼働中です。			|
| F11-2	| リソース 停止					| error	| Resource _prmResource_ : Stopped			| リソースID"_prmResource_"は停止しています。					|
| F11-3	| リソース 開始(配置移動なし)			| info	| Resource _prmResource_ : Started on _pm01_		| リソースID"_prmResource_"はノード"_pm01_"で稼働中です。			|
| F11-9	| リソース 停止(配置移動なし)			| error	| Resource _prmResource_ : Stopped			| リソースID"_prmResource_"は停止しています。					|
| F11-5	| リソース Unmanaged				| error	| Unmanaged resource exists.				| Pacemakerが管理していない(Unmanaged)リソースがあります。			|
| F11-6	| リソース Move					| info	| Resource _prmResource_ : Move _pm01_ -> _pm02_	| リソースID"_prmResource_"はノード"_pm01_"からノード"_pm02_"に移動します。	|
| F11-8	| リソース Restart(配置移動なし)		| info	| Resource _prmResource_ : Started on _pm01_		| リソースID"_prmResource_"はノード"_pm01_"で稼働中です。			|
| F11-11| リソース Recover(配置移動なし)		| info	| Resource _prmResource_ : Started on _pm01_		| リソースID"_prmResource_"はノード"_pm01_"で稼働中です。			|
| F11-12| リソース Reload(配置移動なし)			| info	| Resource _prmResource_ : Started on _pm01_		| リソースID"_prmResource_"はノード"_pm01_"で稼働中です。			|
| F11-13| リソース Recover				| info	| Resource _prmResource_ : Move _pm01_ -> _pm02_	| リソースID"_prmResource_"はノード"_pm01_"からノード"_pm02_"に移動します。	|
| F11-14| リソース Migrate				| info	| Resource _prmResource_ : Move _pm01_ -> _pm02_	| リソースID"_prmResource_"はノード"_pm01_"からノード"_pm02_"に移動します。	|

***
[Pacemakerログ解析支援ツール（pm_logconv-cs-2.4）](../README.md)
