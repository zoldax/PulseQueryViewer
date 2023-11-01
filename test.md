# QRadar Pulse Dashboard Queries

## Widget Number: 1 - Stat Payload EP (GV) (Processor)
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select "LookupHostId(EventProcessorId)" as EP, "COUNT" as mycount, time*1000 as epoch, epoch/(1000*60) as mymin, "AVG_StrLen(UTF8(Payload))" as mypayload, (mypayload*mycount)/(1024*1024) as myTOTALMB from globalview('Pulse-AS-GVStatPayload3','NORMAL') group by mymin, EP order by epoch last 3 HOURS
```

## Widget Number: 2 - Stat Payload EP (GV) (Processor) (Hourly)
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select "LookupHostId(EventProcessorId)" as EP, "COUNT" as mycount, time*1000 as epoch, epoch/(1000*60) as mymin, "AVG_StrLen(UTF8(Payload))" as mypayload, (mypayload*mycount)/(1024*1024) as myTOTALMB from globalview('Pulse-AS-GVStatPayload3','HOURLY') group by mymin, EP order by epoch last 1 DAYS
```

## Widget Number: 3 - Stat Payload EP (GV) (Processor) (Daily)
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select "LookupHostId(EventProcessorId)" as EP, "COUNT" as mycount, time*1000 as epoch, epoch/(1000*60) as mymin, "AVG_StrLen(UTF8(Payload))" as mypayload, (mypayload*mycount)/(1024*1024) as myTOTALMB from globalview('Pulse-AS-GVStatPayload3','DAILY') group by mymin, EP order by epoch last 2 DAYS
```

## Widget Number: 4 - Stat Payload EP (GV) (Processor) (BN)
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select "LookupHostId(EventProcessorId)" as EP, "COUNT" as mycount, time*1000 as epoch, epoch/(1000*60) as mymin, "AVG_StrLen(UTF8(Payload))" as mypayload, (mypayload*mycount)/(1024*1024) as myTOTALMB from globalview('Pulse-AS-GVStatPayload3','NORMAL') group by EP order by myTotalMB desc last 1 HOURS
```

## Widget Number: 5 - Stat Payload EP (GV) (Processor) (BN) (Hourly)
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select "LookupHostId(EventProcessorId)" as EP, "COUNT" as mycount, time*1000 as epoch, epoch/(1000*60) as mymin, "AVG_StrLen(UTF8(Payload))" as mypayload, (mypayload*mycount)/(1024*1024) as myTOTALMB from globalview('Pulse-AS-GVStatPayload3','HOURLY') group by EP order by myTotalMB desc last 2 HOURS
```

## Widget Number: 6 - Stat Payload EP (GV) (Processor) (BN) (Daily)
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select "LookupHostId(EventProcessorId)" as EP, "COUNT" as mycount, time*1000 as epoch, epoch/(1000*60) as mymin, "AVG_StrLen(UTF8(Payload))" as mypayload, (mypayload*mycount)/(1024*1024) as myTOTALMB from globalview('Pulse-AS-GVStatPayload3','DAILY') group by EP order by myTotalMB desc last 2 DAYS
```

## Widget Number: 7 - MB by (GV) (Min)
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select "LookupHostId(EventProcessorId)" as EP, "COUNT" as mycount, time*1000 as epoch, epoch/(1000*60) as mymin, "AVG_StrLen(UTF8(Payload))" as mypayload, (mypayload*mycount)/(1024*1024) as myTOTALMB from globalview('Pulse-AS-GVStatPayload3','NORMAL') group by EP order by myTOTALMB desc
```

## Widget Number: 8 - MB by EP (GV) (HOUR)
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select "LookupHostId(EventProcessorId)" as EP, "COUNT" as mycount, time*1000 as epoch, epoch/(1000*60) as mymin, "AVG_StrLen(UTF8(Payload))" as mypayload, (mypayload*mycount)/(1024*1024) as myTOTALMB from globalview('Pulse-AS-GVStatPayload3','NORMAL') group by EP order by myTOTALMB desc   last 1 HOURS
```

## Widget Number: 9 - MB by EP  (GV) (DAILY)
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select "LookupHostId(EventProcessorId)" as EP, "COUNT" as mycount, time*1000 as epoch, epoch/(1000*60) as mymin, ("AVG_StrLen(UTF8(Payload))") as mypayload, (mypayload*mycount)/(1024*1024) as myTOTALMB from globalview('Pulse-AS-GVStatPayload3','DAILY') group by EP order by myTOTALMB desc  last 2 DAYS
```

## Widget Number: 10 - Moyenne EPS (GV) Jour
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select "AVG_Events per Second Coalesced - Peak 1 Sec" as EPS, "Parent" as EP, time*1000 as epoch, epoch/(1000*60) as mymin from globalview('Event Rate (EPS)','DAILY') group by mymin, EP order by epoch last 90 DAYS 
```

## Widget Number: 11 - EPS / DAY
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select SUM("AVG_Events per Second Coalesced - Peak 1 Sec") as EPS, "Parent" as EP, time*1000 as epoch, epoch/(1000*60) as mymin from globalview('Event Rate (EPS)','DAILY') last 2 DAYS
```

## Widget Number: 12 - Moyenne EPS (GV) Jour (Stack)
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select "AVG_Events per Second Coalesced - Peak 1 Sec" as EPS, "Parent" as EP, time*1000 as epoch, epoch/(1000*60) as mymin from globalview('Event Rate (EPS)','DAILY') group by mymin, EP order by epoch last 90 DAYS 
```

## Widget Number: 13 - Stat Payload EP (GV) (Processor) (BN) (Max Value of AVG)
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select "LookupHostId(EventProcessorId)" as EP, "COUNT" as mycount, time*1000 as epoch, epoch/(1000*60) as mymin, MAX("AVG_StrLen(UTF8(Payload))") as mypayload, (mypayload*mycount)/(1024*1024)/60 as myTOTALMB from globalview('Pulse-AS-GVStatPayload3','NORMAL') group by EP order by myTOTALMB desc  last 1 DAYS
```

## Widget Number: 14 - Moyenne FLOW (GV) Jour
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select "AVG_Flows per Second - Peak 1 Min" as FPS,"Flow Source" as FP,time*1000 as epoch,epoch/(1000*60) as mymin from globalview('Flow Rate (FPS)','DAILY') group by mymin,FP order by epoch last 90 DAYS 
```

## Widget Number: 15 - Moyenne FLOW (GV) Jour (Stack)
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select "AVG_Flows per Second - Peak 1 Min" as FPS,"Flow Source" as FP,time*1000 as epoch,epoch/(1000*60) as mymin from globalview('Flow Rate (FPS)','DAILY') group by mymin,FP order by epoch last 90 DAYS 
```

## Widget Number: 16 - FPS / DAY
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select SUM("AVG_Flows per Second - Peak 1 Min") as FPS, "Flow Source" as FP, time*1000 as epoch, epoch/(1000*60) as mymin from globalview('Flow Rate (FPS)','DAILY') last 2 DAYS
```

## Widget Number: 17 - FPS / DAY (AVG Table)
**Dashboard**: Abakus Sécurité - Stats Processor

```sql
select ("AVG_Flows per Second - Peak 1 Min") as FPS, "Flow Source" as FP, time*1000 as epoch, epoch/(1000*60) as mymin, (FPS)/60 as myTOTALMB from globalview('Flow Rate (FPS)','DAILY') GROUP BY FP order by myTOTALMB desc last 2 DAYS
```

## Widget Number: 1 - Managed Host Event Overview
**Dashboard**: TBD-Pascal-Metriques

```sql
Query not found
```

## Widget Number: 2 - Top 10 log sources by event count
**Dashboard**: TBD-Pascal-Metriques

```sql
SELECT starttime/(1000*60) as minute, (minute * (1000*60)) as stime, DATEFORMAT(starttime,'YYYY MM dd HH:mm:ss') as showTime, logsourcename(logSourceId) AS 'Log Source', SUM("eventCount") AS 'Event Count (Sum)', logsourceid as 'Log Source ID' from events where logsourceid in ( select logsourceid from ( select logsourceid, SUM("eventCount") AS 'Event Count (Sum)' from events where logSourceId not in (63,64,65,67,69) group by logSourceId order by "Event Count (Sum)" limit 10 last 2 hours ) ) GROUP BY minute, logSourceId order by minute ASC last 2 hours
```

