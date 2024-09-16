# -*- coding: utf-8 -*-
import json
import copy
import os
import re

# 保留部分
def document_metric(pre_result, gold_result):
   
    pre_num=0
    gold_num=0
    total_pre_true=0
    file_num=0
    macroP,macroR,macroF=0,0,0
    microP,microR,microF=0,0,0
    for pre_id in pre_result.keys():
        doc_pre=[]
        doc_gold=[]
        for ele in pre_result[pre_id]:
            if ele[2] not in doc_pre:
                doc_pre.append(ele[2])
        for ele in gold_result[pre_id]:
            if ele[2] not in doc_gold:
                doc_gold.append(ele[2])
        file_num+=1
        doc_pre_true=0        
        pre_num+=len(doc_pre)
        gold_num+=len(doc_gold)
        
        for ele in doc_pre:
            if ele in doc_gold:
                total_pre_true+=1
                doc_pre_true+=1
                              
        if len(doc_pre)==0 and len(doc_gold)==0:
            temp_macroP,temp_macroR,temp_macroF=1,1,1
        elif len(doc_pre)==0 and len(doc_gold)!=0:
            temp_macroP,temp_macroR,temp_macroF=0,0,0
        elif len(doc_pre)!=0 and len(doc_gold)==0:
            temp_macroP,temp_macroR,temp_macroF=0,0,0
        elif len(doc_pre)!=0 and len(doc_gold)!=0:
            temp_macroP=doc_pre_true/len(doc_pre)
            temp_macroR=doc_pre_true/len(doc_gold)
            if temp_macroP+temp_macroR==0:
                temp_macroF=0
            else:
                temp_macroF=2*temp_macroP*temp_macroR/(temp_macroP+temp_macroR)
                
        macroP+=temp_macroP
        macroR+=temp_macroR
        macroF+=temp_macroF
    macroP=macroP/file_num
    macroR=macroR/file_num
    if macroP+macroR!=0:
        macroF=2*macroP*macroR/(macroP+macroR)
    else:
        macroF=0
    
    if pre_num==0 and gold_num==0:
        microP,microR,microF=1,1,1
    elif pre_num==0 and gold_num!=0:
        microP,microR,microF=0,0,0
    elif pre_num!=0 and gold_num==0:
        microP,microR,microF=0,0,0
    elif pre_num!=0 and gold_num!=0:    
        microP=total_pre_true/pre_num
        microR=total_pre_true/gold_num
        microF=2*microP*microR/(microP+microR)
    print('......document level evaluation:......')
    # print('file num:',file_num)
    # print(gold_num,pre_num,total_pre_true)
    print('miP=%.5f, miR=%.5f, miF=%.5f' %(microP,microR,microF))
    print('maP=%.5f, maR=%.5f, maF=%.5f' %(macroP,macroR,macroF))
    print('%.5f %.5f %.5f %.5f %.5f %.5f' %(microP,microR,microF,macroP,macroR,macroF))
    return macroF
def mention_metric_new(pre_result, gold_result):

    gold_num=0
    NER_true_num_Ps=0
    NER_true_num_Rs=0
    NER_true_num_Pr=0
    NER_true_num_Rr=0
    pre_num=0
    NEN_true_num_Ps=0
    NEN_true_num_Rs=0
    NEN_true_num_Pr=0
    NEN_true_num_Rr=0
    

    for pmid in pre_result.keys():
        
        doc_pre=copy.deepcopy(pre_result[pmid])
        doc_gold=copy.deepcopy(gold_result[pmid])
        
        gold_num+=len(doc_gold)
        pre_num+=len(doc_pre)
        
        entity_gold={}
        for ele in doc_gold:
            entity_index=ele[0]+' '+ele[1]
            if entity_index not in entity_gold.keys():
                entity_gold[entity_index]=ele[2]
            # else:
                # print('over!!',ele)
        entity_pre={}
        for ele in doc_pre:
            entity_index=ele[0]+' '+ele[1]
            if entity_index not in entity_pre.keys():
                entity_pre[entity_index]=[ele[2]]
            else:
                if ele[2] not in entity_pre[entity_index]:
                    entity_pre[entity_index].append(ele[2])
        
        for pre_ele in doc_pre:
            pre_index=pre_ele[0]+' '+pre_ele[1]
            if pre_index in entity_gold.keys():
                NER_true_num_Ps+=1
                if pre_ele[2] == entity_gold[pre_index]:
                    NEN_true_num_Ps+=1
        
        
        for gold_ele in doc_gold:
            gold_index=gold_ele[0]+' '+gold_ele[1]
            if gold_index in entity_pre.keys():
                NER_true_num_Rs+=1
                if gold_ele[2] in entity_pre[gold_index]:
                    NEN_true_num_Rs+=1
        
        for pre_ele in doc_pre:
            ner_flag=0
            for gold_ele in doc_gold:
                if max(int(pre_ele[0]),int(gold_ele[0])) <= min(int(pre_ele[1]),int(gold_ele[1])):
                    ner_flag=1
                    if pre_ele[2]==gold_ele[2]:
                        NEN_true_num_Pr+=1    
                        break
            if ner_flag==1:
                NER_true_num_Pr+=1
        
        for gold_ele in doc_gold:
            ner_flag=0
            for pre_ele in doc_pre:
                pre_index=pre_ele[0]+' '+pre_ele[1]
                if max(int(pre_ele[0]),int(gold_ele[0])) <= min(int(pre_ele[1]),int(gold_ele[1])):
                    ner_flag=1
                    if gold_ele[2] in entity_pre[pre_index]:
                        NEN_true_num_Rr+=1    
                        break
            if ner_flag==1:
                NER_true_num_Rr+=1
        
       
                
    if pre_num==0 and gold_num==0:
        NER_P_s,NER_R_s,NER_F_s=1,1,1
        NER_P_r,NER_R_r,NER_F_r=1,1,1
        NEN_P_s,NEN_R_s,NEN_F_s=1,1,1
        NEN_P_r,NEN_R_r,NEN_F_r=1,1,1

    elif pre_num==0 and gold_num!=0:
        NER_P_s,NER_R_s,NER_F_s=0,0,0
        NER_P_r,NER_R_r,NER_F_r=0,0,0
        NEN_P_s,NEN_R_s,NEN_F_s=0,0,0
        NEN_P_r,NEN_R_r,NEN_F_r=0,0,0
        
    elif pre_num!=0 and gold_num==0:
        NER_P_s,NER_R_s,NER_F_s=0,0,0
        NER_P_r,NER_R_r,NER_F_r=0,0,0
        NEN_P_s,NEN_R_s,NEN_F_s=0,0,0
        NEN_P_r,NEN_R_r,NEN_F_r=0,0,0
    elif pre_num!=0 and gold_num!=0:
        
        NER_P_s=NER_true_num_Ps/pre_num
        NER_P_r=NER_true_num_Pr/pre_num
        NEN_P_s=NEN_true_num_Ps/pre_num
        NEN_P_r=NEN_true_num_Pr/pre_num
        
        NER_R_s=NER_true_num_Rs/gold_num
        NER_R_r=NER_true_num_Rr/gold_num
        NEN_R_s=NEN_true_num_Rs/gold_num
        NEN_R_r=NEN_true_num_Rr/gold_num

        NER_F_s=2*NER_P_s*NER_R_s/(NER_P_s+NER_R_s+0.000001)
        NER_F_r=2*NER_P_r*NER_R_r/(NER_P_r+NER_R_r+0.000001)
        NEN_F_s=2*NEN_P_s*NEN_R_s/(NEN_P_s+NEN_R_s+0.000001)
        NEN_F_r=2*NEN_P_r*NEN_R_r/(NEN_P_r+NEN_R_r+0.000001)
        
    print('......memtion level evaluation:......')
    #print(gold_num,pre_num)
    # print('NER P_s=%.5f, R_s=%.5f, F_s=%.5f' %(NER_P_s,NER_R_s,NER_F_s))
    print('NER P_r=%.5f, R_r=%.5f, F_r=%.5f' %(NER_P_r,NER_R_r,NER_F_r))  
    # print('NEN P_s=%.5f, R_s=%.5f, F_s=%.5f' %(NEN_P_s,NEN_R_s,NEN_F_s))
    print('NEN P_r=%.5f, R_r=%.5f, F_r=%.5f' %(NEN_P_r,NEN_R_r,NEN_F_r))
    print('%.5f %.5f %.5f %.5f %.5f %.5f' %(NER_P_r,NER_R_r,NER_F_r,NEN_P_r,NEN_R_r,NEN_F_r))
    return NEN_F_r
# 保留部分

# 读取预测的结果 假定pmid在第一行中
def read_files_in_directory(directory):
    all_pre = []
    # 遍历目录中的文件
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # 检查路径是否为文件
        if os.path.isfile(filepath):
            # 检查文件后缀
            if not filename.endswith('.neg2.PubTator'):
                # 打开文件并读取内容
                with open(filepath, 'r') as fin:
                    content = fin.read().strip().split('\n\n')
                    all_pre.extend(content)

    return all_pre

# 读取GT 并添加pmid
def read_files_in_directory_add_name(directory):
    all_gold = []
    # 遍历目录中的文件
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # 检查路径是否为文件
        if os.path.isfile(filepath):
            # 获取文件名中的数字部分
            numbers = ''.join(re.findall(r'\d+', filename))
            # 打开文件并读取内容
            with open(filepath, 'r') as fin:
                content = fin.read().strip()
                # 将数字部分添加到内容前面
                content_with_numbers = f"{numbers}\n{content}"
                all_gold.append(content_with_numbers)

    return all_gold

# GSCplus数据集
def GSCplus(prefile,goldfile,subtree=True):
    # 保留部分
    fin_alt=open('../dict/alt_hpoid.json','r',encoding='utf-8')
    fin_subtree=open('../dict/lable.vocab','r',encoding='utf-8')
    alt_hpoid=json.load(fin_alt)
    fin_alt.close()
    subtree_list=fin_subtree.read().strip().split('\n')
    fin_subtree.close()
    # 保留部分
    print()
    print('+++++++++')
    print('[GSCplus]')
    print('+++++++++')

    all_pre=read_files_in_directory(prefile)
    all_gold=read_files_in_directory_add_name(goldfile)
    pre_result={}
    gold_result={}
    for doc_pre in all_pre:
        lines=doc_pre.split('\n')
        pmid=int(lines[0].split('|a|')[0])
        temp_result=[]
        for i in range(1,len(lines)):
            seg=lines[i].split('\t')
            if seg[5] in alt_hpoid.keys():
                hpoid=alt_hpoid[seg[5]]
                if subtree==True:
                    if hpoid in subtree_list:
                        temp_result.append([seg[1],seg[2],hpoid])
                else:
                    temp_result.append([seg[1],seg[2],hpoid])
            # else:
            #     print('pre hpo obo no this id:',lines[i],seg[5])

        pre_result[pmid]=temp_result

    for doc_gold in all_gold:
        lines=doc_gold.split('\n')
        pmid=int(lines[0])
        temp_result=[]
        for i in range(1,len(lines)):
            seg=lines[i].split('\t')
            numbers = re.findall(r'\d+', seg[0])
            hpid = seg[1].split('|')[0].strip().replace('_',':')
            if hpid in alt_hpoid.keys():
                hpoid=alt_hpoid[hpid]
                if subtree==True:
                    if hpoid in subtree_list:
                        temp_result.append([numbers[0],numbers[1],hpoid])
                else:
                    temp_result.append([numbers[0],numbers[1],hpoid])
            else:
                print('gold hpo obo no this id:',lines[i],hpid)
        gold_result[pmid]=temp_result
    
    doc_f=document_metric(pre_result,gold_result)
    men_f=mention_metric_new(pre_result,gold_result)
    return doc_f+men_f

# ID68数据集
def ID68(prefile,goldfile,subtree=True):
    # 保留部分
    fin_alt=open('../dict/alt_hpoid.json','r',encoding='utf-8')
    fin_subtree=open('../dict/lable.vocab','r',encoding='utf-8')
    alt_hpoid=json.load(fin_alt)
    fin_alt.close()
    subtree_list=fin_subtree.read().strip().split('\n')
    fin_subtree.close()
    # 保留部分
    print()
    print('+++++++++')
    print('[ID68]')
    print('+++++++++')

    all_pre=read_files_in_directory(prefile)
    all_gold=read_files_in_directory_add_name(goldfile)
    pre_result={}
    gold_result={}
    for doc_pre in all_pre:
        lines=doc_pre.split('\n')
        pmid=int(lines[0].split('|a|')[0])
        temp_result=[]
        for i in range(1,len(lines)):
            seg=lines[i].split('\t')
            if seg[5] in alt_hpoid.keys():
                hpoid=alt_hpoid[seg[5]]
                if subtree==True:
                    if hpoid in subtree_list:
                        temp_result.append([seg[1],seg[2],hpoid])
                else:
                    temp_result.append([seg[1],seg[2],hpoid])
            # else:
            #     print('pre hpo obo no this id:',lines[i],seg[5])

        pre_result[pmid]=temp_result

    for doc_gold in all_gold:
        lines=doc_gold.split('\n')
        pmid=int(lines[0])
        temp_result=[]
        for i in range(1,len(lines)):
            seg=lines[i].split('\t')
            if seg[3] in alt_hpoid.keys():
                hpoid=alt_hpoid[seg[3]]
                if subtree==True:
                    if hpoid in subtree_list:
                        temp_result.append([seg[0],seg[1],hpoid])
                else:
                    temp_result.append([seg[0],seg[1],hpoid])
            else:
                print('gold hpo obo no this id:',lines[i],seg[3])
        gold_result[pmid]=temp_result
    doc_f=document_metric(pre_result,gold_result)
    men_f=mention_metric_new(pre_result,gold_result)
    return doc_f+men_f

# COPD数据集 
def COPD(prefile,goldfile,subtree=True):
    # 保留部分
    fin_alt=open('../dict/alt_hpoid.json','r',encoding='utf-8')
    fin_subtree=open('../dict/lable.vocab','r',encoding='utf-8')
    alt_hpoid=json.load(fin_alt)
    fin_alt.close()
    subtree_list=fin_subtree.read().strip().split('\n')
    fin_subtree.close()
    # 保留部分
    print()
    print('+++++++++')
    print('[COPD]')
    print('+++++++++')

    all_pre=read_files_in_directory(prefile)
    all_gold=read_files_in_directory_add_name(goldfile)
    pre_result={}
    gold_result={}
    for doc_pre in all_pre:
        lines=doc_pre.split('\n')
        pmid=int(lines[0].split('|a|')[0])
        temp_result=[]
        for i in range(1,len(lines)):
            seg=lines[i].split('\t')
            if seg[5] in alt_hpoid.keys():
                hpoid=alt_hpoid[seg[5]]
                if subtree==True:
                    if hpoid in subtree_list:
                        temp_result.append([seg[1],seg[2],hpoid])
                else:
                    temp_result.append([seg[1],seg[2],hpoid])
            # else:
            #     print('pre hpo obo no this id:',lines[i],seg[5])

        pre_result[pmid]=temp_result

    for doc_gold in all_gold:
        lines=doc_gold.split('\n')
        pmid=int(lines[0])
        temp_result=[]
        for i in range(1,len(lines)):
            seg=lines[i].split('\t')
            # 统一接口获取begin end hpoid
            temp_numbers = re.findall(r'\d+', seg[0])
            if len(temp_numbers) < 1:
                continue
            temp_begin = temp_numbers[1]
            temp_end = temp_numbers[2]
            temp_hpoid = seg[0].split('|')[0].strip().replace('_',':')

            if temp_hpoid in alt_hpoid.keys():
                hpoid=alt_hpoid[temp_hpoid]
                if subtree==True:
                    if hpoid in subtree_list:
                        temp_result.append([temp_begin,temp_end,hpoid])
                else:
                    temp_result.append([temp_begin,temp_end,hpoid])
            else:
                print('gold hpo obo no this id:',lines[i],temp_hpoid)
        gold_result[pmid]=temp_result
    doc_f=document_metric(pre_result,gold_result)
    men_f=mention_metric_new(pre_result,gold_result)
    return doc_f+men_f

# BIOASQ数据集
def BIOASQ(prefile,goldfile,subtree=True):
    # 保留部分
    fin_alt=open('../dict/alt_hpoid.json','r',encoding='utf-8')
    fin_subtree=open('../dict/lable.vocab','r',encoding='utf-8')
    alt_hpoid=json.load(fin_alt)
    fin_alt.close()
    subtree_list=fin_subtree.read().strip().split('\n')
    fin_subtree.close()
    # 保留部分
    print()
    print('+++++++++')
    print('[BIOASQ]')
    print('+++++++++')

    all_pre=read_files_in_directory(prefile)
    all_gold=read_files_in_directory_add_name(goldfile)
    pre_result={}
    gold_result={}
    for doc_pre in all_pre:
        lines=doc_pre.split('\n')
        pmid=int(lines[0].split('|a|')[0])
        temp_result=[]
        for i in range(1,len(lines)):
            seg=lines[i].split('\t')
            if seg[5] in alt_hpoid.keys():
                hpoid=alt_hpoid[seg[5]]
                if subtree==True:
                    if hpoid in subtree_list:
                        temp_result.append([seg[1],seg[2],hpoid])
                else:
                    temp_result.append([seg[1],seg[2],hpoid])
            # else:
            #     print('pre hpo obo no this id:',lines[i],seg[5])

        pre_result[pmid]=temp_result

    for doc_gold in all_gold:
        lines=doc_gold.split('\n')
        pmid=int(lines[0])
        temp_result=[]
        for i in range(2,len(lines)):
            seg=lines[i].split(',')
            # 统一接口获取begin end hpoid
            temp_begin = seg[0]
            temp_end = seg[1]
            temp_hpoid = seg[4]

            if temp_hpoid in alt_hpoid.keys():
                hpoid=alt_hpoid[temp_hpoid]
                if subtree==True:
                    if hpoid in subtree_list:
                        temp_result.append([temp_begin,temp_end,hpoid])
                else:
                    temp_result.append([temp_begin,temp_end,hpoid])
            else:
                print('gold hpo obo no this id:',lines[i],temp_hpoid)
        gold_result[pmid]=temp_result
    doc_f=document_metric(pre_result,gold_result)
    men_f=mention_metric_new(pre_result,gold_result)
    return doc_f+men_f

# NCBI数据集
def NCBI(prefile,goldfile,subtree=True):
    # 保留部分
    fin_alt=open('../dict/alt_hpoid.json','r',encoding='utf-8')
    fin_subtree=open('../dict/lable.vocab','r',encoding='utf-8')
    alt_hpoid=json.load(fin_alt)
    fin_alt.close()
    subtree_list=fin_subtree.read().strip().split('\n')
    fin_subtree.close()
    # 保留部分
    print()
    print('+++++++++')
    print('[NCBI]')
    print('+++++++++')

    all_pre=read_files_in_directory(prefile)
    all_gold=read_files_in_directory_add_name(goldfile)
    pre_result={}
    gold_result={}
    for doc_pre in all_pre:
        lines=doc_pre.split('\n')
        pmid=int(lines[0].split('|a|')[0])
        temp_result=[]
        for i in range(1,len(lines)):
            seg=lines[i].split('\t')
            if seg[5] in alt_hpoid.keys():
                hpoid=alt_hpoid[seg[5]]
                if subtree==True:
                    if hpoid in subtree_list:
                        temp_result.append([seg[1],seg[2],hpoid])
                else:
                    temp_result.append([seg[1],seg[2],hpoid])
            # else:
            #     print('pre hpo obo no this id:',lines[i],seg[5])

        pre_result[pmid]=temp_result

    for doc_gold in all_gold:
        lines=doc_gold.split('\n')
        pmid=int(lines[0])
        temp_result=[]
        for i in range(2,len(lines)):
            seg=lines[i].split(',')
            # 统一接口获取begin end hpoid
            temp_begin = seg[0]
            temp_end = seg[1]
            temp_hpoid = seg[4]

            if temp_hpoid in alt_hpoid.keys():
                hpoid=alt_hpoid[temp_hpoid]
                if subtree==True:
                    if hpoid in subtree_list:
                        temp_result.append([temp_begin,temp_end,hpoid])
                else:
                    temp_result.append([temp_begin,temp_end,hpoid])
            # else:
            #     print('gold hpo obo no this id:',lines[i],temp_hpoid)
        gold_result[pmid]=temp_result
    doc_f=document_metric(pre_result,gold_result)
    men_f=mention_metric_new(pre_result,gold_result)
    return doc_f+men_f

import sys
if __name__=='__main__':
    
    f = open('/root/autodl-tmp/pubmedbert_COPDdev_hybrid.log', 'a')
    sys.stdout = f

    pre_path='/root/autodl-tmp/PHENOTAGGER/output/pubmedbert_COPDdev_hybrid/'
    gold_path='/root/autodl-tmp/Gold/'
    #GSCplus(pre_path+'GSCplus', gold_path+'gscplus_gold', subtree=True)
    #ID68(pre_path+'ID-68', gold_path+'id68_gold', subtree=True)
    COPD(pre_path+'COPD', gold_path+'copd_gold', subtree=True)
    #BIOASQ(pre_path+'BIOASQ', gold_path+'bioasq_gold', subtree=True)
    #NCBI(pre_path+'NCBI', gold_path+'ncbi_gold', subtree=True)