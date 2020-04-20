createDelProc='''
create or replace procedure likai_delPyfaxx(v_pyfaxx_id varchar2)
as
  begin
    delete
    from JW_JH_PYFAKCXSDZB dzb
    where exists(select 1
                 from JW_JH_PYFAXXB pyfa,
                      JW_JH_PYFAXFYQXXB xfb,
                      JW_JH_PYFAKCXXB kcxx
                 where pyfa.PYFAXX_ID = v_pyfaxx_id
                   and pyfa.PYFAXX_ID = xfb.PYFAXX_ID
                   and xfb.XFYQJD_ID = kcxx.XFYQJD_ID
                   and kcxx.PYFAKCXX_ID = dzb.PYFAKCXX_ID
              );
    commit;
    delete
    from JW_JH_PYFAKCXXB kcxx
    where exists(select 1
                 from JW_JH_PYFAXXB pyfa,
                      JW_JH_PYFAXFYQXXB xfb
                 where pyfa.PYFAXX_ID = v_pyfaxx_id
                   and xfb.XFYQJD_ID = kcxx.XFYQJD_ID);
    commit;
    delete
    from JW_JH_PYFAXFYQXXB xfb
    where exists(select 1 from JW_JH_PYFAXXB pyfa where pyfa.PYFAXX_ID = v_pyfaxx_id
                                                    and pyfa.PYFAXX_ID = xfb.PYFAXX_ID);
    commit;
    delete from JW_JH_PYFASYNJB where PYFAXX_ID = v_pyfaxx_id;
    commit;
    delete from JW_JH_PYFAXXB where PYFAXX_ID = v_pyfaxx_id;
    commit;
  end;
'''
def delPyfa(con,nj):
    con.execute(createDelProc)
    code='''select PYFAXX_ID from JW_JH_PYFASYNJB where NJDM_ID='{}' and 1=1;'''.format(nj)
    pyfaxx_ids=con.execute(code)
    for pyfaxx_id in pyfaxx_ids:
        ##删除培养方案信息分表
        con.execute('likai_delPyfaxx',[pyfaxx_id])
        print(pyfaxx_id,'已删除')
    con.execute('''drop procedure likai_delPyfaxx''')
    return 1
