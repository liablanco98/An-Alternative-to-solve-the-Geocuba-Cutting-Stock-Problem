from .definitions import Piece, Stock


def fits(piece:Piece,sheets:list[tuple[tuple[int,int],list[tuple[tuple[int,int],Piece]]]],offset_l:int,stock_w:int):
    p_l=piece.length
    p_w=piece.width

    if len(sheets):
        sheets.sort(key=lambda x:x[0][0])    
        for i in range(len(sheets)):
            sheet=sheets[i]
            l=sheet[0][0]
            w=sheet[0][1]
            elems=sheet[1]

            if p_l>l and (p_l-l)>offset_l:
                #do not fit
                return False,offset_l,sheets

            elif p_w>w:
                #try next
                continue

            pos_elem=elems[-1][0]    
            last_w=pos_elem[1]
            item_pos=(p_l,last_w+p_w)
            elems.append((item_pos,piece))
            del sheets[i]
            
            if p_l>l:
                #extend
                sheet_temp=((p_l,w-p_w),elems)
                offset_l=offset_l-(p_l-l)

            else:
                #append 
                sheet_temp=((l,w-p_w),elems)

            sheets.append(sheet_temp)
            return True, offset_l,sheets

        # l=((p_l,stock_w-p_w),[(p_l,p_w)])
        # sheets.append(l)
        # return True, offset_l-p_l,sheets
        
    #Starting sheets
    l=((p_l,stock_w-p_w),[((p_l,p_w),piece)])
    sheets.append(l)
    return True, offset_l-p_l,sheets


# building rows sheets
def heuristic_2(items:list[Piece],stock:Stock)->list[tuple[tuple[int,int],tuple[int,int],Piece]]:
    m:int=len(items)
    builded:list[tuple[tuple[int,int],list[tuple[tuple[int,int],Piece]]]]=[]

    s_l=stock.length
    s_w=stock.width
    
    for itm in items:
        valid,s_l,builded=fits(itm, builded,s_l,s_w)
        if not valid:
            break

    curr_l=0
    result:list[tuple[tuple[int,int],tuple[int,int],Piece]]=[]
    for b in builded:
        curr_b_w=0
        curr_b_l=0
        
        for lis in b:
            pos_l=lis[0][0]
            pos_w=lis[0][1]
            piece=lis[1]

            new_tup=((curr_l,curr_b_w),(curr_l+pos_l,pos_w),piece)
            result.append(new_tup)
            curr_b_w=pos_w
            if pos_l>curr_b_l:
                curr_b_l=pos_l

        curr_l+=curr_b_l

    return result