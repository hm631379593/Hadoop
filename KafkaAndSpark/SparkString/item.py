CODE 		SEGMENT            		;H8279.ASM
ASSUME 	CS:	CODE
D8279   EQU    0FF80H
C8279   EQU    0FF81H
   	ORG 2A90H
   	JMP START
KH     DB ?             ;键号,KEY HAO
ZW     DB ?
ZX     DB ?
START: 	MOV DX,C8279     			;8279命令口,WR-->MODE
       	MOV AL,00H
       	OUT DX,AL					;8位,左入口,编码,双键锁定
       	MOV AL,32H       			;时钟分频
       	OUT DX,AL
       	MOV AL,0DFH      			;清除命令,CLR BUF
       	OUT DX,AL
WAIT:  	IN AL,DX         			;clr buf end ?
       	TEST AL,80H
       	JNZ WAIT					;未清完转等
       	MOV AL,85H 				;写显示内存地址
       OUT DX,AL
       MOV DX,D8279     			;字形代码口,ff80H
       MOV AL,0C8H
       OUT DX,AL					;写’P’
START0:	MOV ZW,85H       			;字位寄存器初值(最高位)
NEXT:  	MOV KH,00H       			;键号:00~13H
       	MOV DX,C8279     			;读8279状态字,RD STATUS KEY ?
NOKEY: 	IN AL,DX
       	AND AL,07H
       	CMP AL,00H
       	JZ NOKEY					;为零无键转
       	MOV DX,D8279     			;rd key zhi
       	IN AL,DX					;读键值
       		MOV AH,AL        			;存键值,SAVE KEY ZHI
       		MOV BX,OFFSET TABK		;键值表首址
CMPK:  	MOV AL,KH
       XLAT						;查表
       CMP AH,AL
       JZ KEY						;键值处理
       INC KH						;键号加1
       CMP KH,14H
       JNC KEY0					;大于14视无键转
       JMP CMPK					;继续比较
KEY:   	CMP KH,10H
       JNC FUN					;大于等于10,转功能键处理
       CALL DIS					;数字键,调显示
       DEC ZW						;指向下一位
KEY0:  	CMP ZW,7FH					;末位代码
       JNZ NEXT					;未到末位转
       JMP START0					;六位显示完转
FUN:   	CMP KH,13H					;功能键处理
       	JNZ KEY0					;不是[MON]键转
        	MOV ZW,85H					;置最高位Ram地址
       	MOV KH,08H					; ’8’
       	CALL DIS					;
       	MOV ZW,84H
       	MOV KH,02H					;’2’
       	CALL DIS
       	MOV ZW,83H
       	MOV KH,07H					;’7’
       	CALL DIS
       	MOV ZW,82H
       	MOV KH,09H					;’9’
       	CALL DIS
       	MOV ZW,81H
       	MOV KH,11H					;‘-‘
       	CALL DIS
       	MOV ZW,80H
       	MOV KH,11H					;’-’
       	CALL DIS
;--------------------
       	CALL DELY
       	MOV ZW,85H
       	MOV KH,09H					;’g’
       	CALL DIS
       	MOV ZW,84H
       	MOV KH,00H					;’o’
       	CALL DIS
       	MOV ZW,83H
       	MOV KH,00H					;’o’
       	CALL DIS
       	MOV ZW,82H
       	MOV KH,0DH					;’d’
       	CALL DIS
       	MOV ZW,81H
       	MOV KH,10H					;’ ’
       	CALL DIS
       	MOV ZW,80H
       	MOV KH,10H					;’ ’
       	CALL DIS
       	JMP $
DIS:   	MOV DX,C8279       		;显示RAM地址:85H,84H,..80H
       MOV AL,ZW					;位码
       OUT DX,AL					;输出位码
       MOV AL,KH        			;字形代码,WR CODE
       MOV BX,OFFSET TABC		;字形表首址
       XLAT						;查表
       MOV DX,D8279  			;8279数据口,ff80H
       OUT DX,AL					;写字形代码
       RET
DELY:  	MOV BX,00FFH
DELY1: 	DEC BX
       CMP BX,0000
       JZ  DELY2
       MOV CX,04FFH
       LOOP $
       JMP DELY1
DELY2: 	RET
TABK:		DB 0C9H,0C1H,0D1H,0E1H,0C8H,0D8H,0E8H,0C0H,0D0H
			DB 0E0H,0F0H,0F8H,0F1H,0F9H,0E9H,0D9H
        		DB 0F2H,0FAH,0F3H,0FBH				;键值表
TABC:		DB 0CH,9FH,4AH,0BH,99H,29H,28H,8FH,08H,09H,88H
			DB 38H,6CH,1AH,68H,0E8H,0FFH,0FBH	;字形代码表

CODE ENDS
END  START
