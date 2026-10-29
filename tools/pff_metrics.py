"""PFF Ultimate season stats -> Roster Lab board metrics (db = sample, m = the 4 graded metrics, in board order).

Input `p` is one player's 2026 season pull from PFF Ultimate, grouped by the PFF report it came from:
  rec / sep (receiving + separation), rush / brk (rushing + breakaway), pass / clean / excl (passing, clean pocket,
  passes excluding throwaways/spikes), gdP / gdR (pass / run play grading: snap, raw_grade_positive, raw_grade_negative),
  ol / pp / tpsPP (offensive line, pass pro, true pass sets), def / rd / pr / tpsPR (defense, run defense, pass rush,
  true pass sets), cov (coverage), ttt (coverage on throws under 2.5s), wide (outside-CB coverage), box (box coverage),
  al (alignment snaps). Each group is the raw PFF row for that report, or None.
Field names are PFF's. Board metric order and meaning come from POSITIONS[k].metrics in index.html; keep them in sync.
No player data lives in this repo.
"""
import re
def g(o,k,d=None):
    return (o or {}).get(k,d)
def r(v,dp=1):
    return None if v is None else round(v,dp)
def div(a,b):
    return None if a is None or not b else a/b
POSMAP={'QB':'QB','HB':'RB','FB':'RB','WR':'WR','TE':'TE','T':'OT','G':'IOL','C':'IOL','DI':'DT','ED':'DE','LB':'LB','S':'SAF','CB':'CB'}
def metrics(p,k):
    if k=='QB':
        db=g(p['pass'],'pass_dropback');gd=p['gdP'] or {}
        att=g(p['pass'],'pass_attempt',0);ex=g(p['excl'],'pass_attempt',0)
        ac=div((g(p['pass'],'pass_complete',0)+g(p['pass'],'pass_drop',0))*100,att-ex)
        return db,[r(div(100*g(gd,'raw_grade_negative',0),db)),r(div(100*g(gd,'raw_grade_positive',0),db)),g(p['clean'],'grades_pass'),r(ac)]
    if k=='RB':
        a=g(p['rush'],'rushing_play')
        return a,[r(div(g(p['rush'],'rushing_avoided_tackle',0),a),2),r(g(p['rush'],'rushing_yards_after_contact_per_carry'),2),r(g(p['rush'],'rushing_yards_per_carry'),1),r(div(g(p['brk'],'rushing_play',0),a),3)]
    if k=='WR':
        rs=g(p['rec'],'route_run_snap');t=g(p['rec'],'receiving_target')
        return rs,[r(div(g(p['rec'],'receiving_yards'),rs),2),g(p['rec'],'grades_pass_route'),r(g(p['rec'],'receiving_yards_after_per_catch'),1),r(div(100*g(p['sep'],'receiving_target',0),t),1)]
    if k=='TE':
        rs=g(p['rec'],'route_run_snap');gd=p['gdR'] or {};s=g(gd,'snap')
        return rs,[r(div(g(p['rec'],'receiving_yards'),rs),2),r(div(100*g(gd,'raw_grade_negative',0),s)),r(div(100*g(gd,'raw_grade_positive',0),s)),r(g(p['rec'],'receiving_yards_after_per_catch'),1)]
    if k in('IOL','OT'):
        gd=p['gdR'] or {};s=g(gd,'snap')
        return g(p['ol'],'off_snaps_1'),[g(p['tpsPP'],'grades_pass_block'),g(p['ol'],'grades_run_block'),g(p['pp'],'pass_block_efficiency',g(p['ol'],'pass_block_efficiency')),r(div(100*g(gd,'raw_grade_negative',0),s))]
    d=p['def'] or {};sn=g(d,'defense_regular_snap');rd=p['rd'] or {}
    stop=r(div(100*g(rd,'stop',0),g(rd,'run_defense_snap')));mt=g(d,'missed_tackle',0);tk=g(d,'tackle',0)+g(d,'tackle_assist',0);mtp=r(div(100*mt,mt+tk))
    if k in('DT','DE'):
        pw=g(p['pr'],'pass_rush_win_percentage')
        return sn,[stop,g(rd,'grades_run_defense'),r(None if pw is None else 100*pw),g(p['tpsPR'],'grades_pass_rush_defense')]
    if k=='LB':
        return sn,[stop,g(rd,'grades_run_defense'),g(p['box'],'grades_coverage_defense'),mtp]
    if k=='SAF':
        c=p['cov'] or {};cp=g(c,'allowed_reception_percentage')
        return sn,[g(c,'grades_coverage_defense'),g(p['ttt'],'grades_coverage_defense'),mtp,r(None if cp is None else 100*cp)]
    if k=='CB':
        w=p['wide'] or {};cp=g(w,'allowed_reception_percentage')
        return sn,[g(w,'grades_coverage_defense'),r(div(g(w,'yards_against'),g(w,'coverage_snap')),2),r(div(100*g(w,'forced_incompletion',0),g(w,'primary_coverage'))),r(None if cp is None else 100*cp)]

POS_FOR_BOARD=POSMAP  # PFF position -> board (CBs who mostly play the slot are NIC, which has no board yet)
