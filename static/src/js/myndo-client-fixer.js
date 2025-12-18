


fetch(document.location.protocol+'//'+document.location.host.replace('odoo.','')+'/fapi/config/get_config').then(response => response.json()).then(data => {console.log(data);
		if(!window.FIXER){window.FIXER={CONFIG:null,
			init:function(data){this.CONFIG=data;
				this.basicurl=document.location.protocol+'//'+document.location.host.replace('8069','80').replace('odoo.','');
				this.NODEHOST=this.basicurl+'/fapi/fixer';
			},
			FIX_ADD_ALIAS:function(ev){
				let addto=ev.target.innerHTML.split(' to column ')[1].replace(/"/g,'');
				let newalias=ev.target.parentElement.parentElement.firstChild.innerHTML;
				if(!newalias){newalias=''};
				newalias=newalias.trim();
				if(newalias==''){
					prompt('Scegliere un valore...');
				}else{
					newalias=newalias.toLowerCase().trim().replace(/,/g,'');
					console.log('Adding alias ('+newalias+') to column ('+addto+')');
					console.log('Adding alias ('+newalias+') to column id ['+ALLCOLS[ALLNAMES[addto]].id+']');
					ALLNAMES[newalias]=ALLNAMES[addto];
					var url=this.NODEHOST.replace('8069','80')+"/fix_add_alias?onload="+encodeURIComponent('window.FIXER._FIX_ADD_ALIAS')+"&newalias="+encodeURIComponent(newalias)+'&cid='+ALLCOLS[ALLNAMES[addto]].id
					console.log(url);
					it3.ins(document.head,'script',['src',url]);
				}
			},
			_FIX_ADD_ALIAS:function(){
				this._PRECHECK(this.LASTIMPORTHEAD,this.LASTIMPORTTEXT,this.LASTIMPORTSEP);
			},
			FIX_CREATE_COL:function(ev){
				let newcolname=ev.target.parentElement.parentElement.firstChild.innerHTML;
				let newform='<form id="newcoljs" action="'+this.NODEHOST.replace('8069','80')+'/fix_add_new_column" method="GET" onsubmit="window.FIXER._FIX_CREATE_COL_OK">Nome: <input name="name" type="text" readonly="readonly" value="'+newcolname.toLowerCase().trim().replace(/,/g,'')+'" /><br/>';		
				newform=newform+'DB type: <select name="dbtype"><option value="jdata">jdata</option><option value="dbdata">dbdata</option><option value="virtual">virtual</option></select><br/>';
				newform=newform+'Type: <select name="type"><option value="string">string</option><option value="int">int</option><option value="float">float</option><option value="percent">percent</option>';
				newform=newform+'<option value="date">date</option><option value="timespan">timespan</option><option value="omit">omit</option>'
				newform=newform+'</select><br/>';
				newform=newform+'Parser: <select name="parser">';
				for(let p=0;p<this.CONFIG.ALLPARSERS.length;p++){newform=newform+'<option value="'+this.CONFIG.ALLPARSERS[p].id+'">'+this.CONFIG.ALLPARSERS[p].name+'</option>'}
				newform=newform+'</select><br/>';
				newform=newform+'Aliases: <input name="alias" type="text" value="" /><br/>';
				newform=newform+'Accept nulls: <input type="checkbox" value="true" name="acceptnulls"/><br/>';
				newform=newform+'Accept nulls but warn: <input type="checkbox" value="true" name="acceptnulls_butwarn" /><br/>';
				newform=newform+'<br/><button onclick="window.FIXER._FIX_CREATE_COL_OK(event)">Create</button><button onclick="window.FIXER._FIX_CREATE_COL_KO(event)">Cancel</button></form>';
				this.LASTDIALOG=it3.ins(document.body,'div',['class','flower_dialog'],newform);
			},
			_FIX_CREATE_COL_OK:function(ev){it3.fix(ev);
				let ss=jQuery('#newcoljs').serialize();
				var url=this.NODEHOST.replace('8069','80')+"/fix_add_new_column?onload="+encodeURIComponent('window.FIXER._FIX_CREATE_COL')+"&"+ss;
				it3.ins(document.head,'script',['src',url]);
				return false;
			},
			_FIX_CREATE_COL_KO:function(ev){
				document.body.removeChild(this.LASTDIALOG);
			},
			_FIX_CREATE_COL:function(data){
				let C=data[0];
				for(let p=0;p<this.CONFIG.ALLPARSERS.length;p++){
					if(this.CONFIG.ALLPARSERS[p].id==C.parser){C.type=this.CONFIG.ALLPARSERS[p].name}
				}
				ALLCOLS.push(C);
				ALLNAMES[C.name.toLowerCase().trim().replace(/,/g,'')]=ALLCOLS.length-1;
				document.body.removeChild(this.LASTDIALOG);
				this._PRECHECK(this.LASTIMPORTHEAD,this.LASTIMPORTTEXT,this.LASTIMPORTSEP);
			},
			FIX_ADD_TO_VALIDATOR:function(ev,urlencodedvalue,validator_id,create_new){
				let tmpuid=it3.uid();let onedone=false;
				if(create_new){
					let inp=it3.ins(ev.target.parentElement,'input',['list',tmpuid+'-list','id','tmpuid-tx','autocomplete','off','value',decodeURIComponent(urlencodedvalue)],false,ev.target);
					console.log('urlencodedvalue '+urlencodedvalue)
					it3.ins(ev.target.parentElement,'hr',[],false,ev.target);
					// let sel=it3.ins(ev.target.parentElement,'select',['id',tmpuid+'-list'],false,ev.target);
					let div=it3.ins(ev.target.parentElement,'div',['id',tmpuid+'-list','style','max-height:30vh;overflow-y:auto'],false,ev.target);
					let dones={};
					for(let v in this.CONFIG.ALLVALIDATORS[validator_id]){
						if(!dones[this.CONFIG.ALLVALIDATORS[validator_id][v]]&&v!='__ValidatorName'){dones[this.CONFIG.ALLVALIDATORS[validator_id][v]]=true;
							// if(onedone){it3.ins(sel,'option',['value',myndo.validator[validator_id][v]],myndo.validator[validator_id][v]);}
							// else{onedone=true;it3.ins(sel,'option',['value',myndo.validator[validator_id][v],'selected','selected'],myndo.validator[validator_id][v]);}
							let indiv=it3.ins(div,'div',['class','result-option'],'');
							let sp=it3.ins(indiv,'span',[],this.CONFIG.ALLVALIDATORS[validator_id][v]);
							indiv.addEventListener('click',ev=>{ev.stopPropagation();
								let val=ev.target.innerHTML;
								if(ev.target.firstElementChild){if(ev.target.firstElementChild.nodeName=="SPAN"){val=ev.target.firstElementChild.innerHTML}}
								// $("input[name='result_value'].o_field_char.o_field_widget.o_input").val(val).focus().change();
								inp.value=val;
							});
						}
					}
					it3.ins(ev.target.parentElement,'hr',[],false,ev.target);
					inp.addEventListener('keyup',function(ev){let foundone=false;
						for(let o=0;o<div.children.length;o++){if(div.children[o].firstElementChild.innerHTML.toLowerCase().indexOf(ev.target.value.toLowerCase())>-1){foundone=true;div.children[o].style.display=''}else{div.children[o].style.display='none'}}
						// if(!foundone){alert('this value doesn\'t exist in this validator;if you want to add it send a request')}
					});
					ev.target.setAttribute('onclick',ev.target.getAttribute('onclick').replace('FIX_ADD','REAL_FIX_ADD'));
				}else{this.REAL_FIX_ADD_TO_VALIDATOR(ev,urlencodedvalue,validator_id,)}
				return false;
			},
			REAL_FIX_ADD_TO_VALIDATOR:function(ev,urlencodedvalue,validator_id,create_new){
				if(create_new){console.log(ev);
					let chosen=ev.target.parentElement.firstElementChild.value;
					if(!chosen){chosen=''};
					let found=false;chosen=chosen.trim();
					for(let v in this.CONFIG.ALLVALIDATORS[validator_id]){if(chosen==this.CONFIG.ALLVALIDATORS[validator_id][v]){found=true;break;}}
					// if(!found){
					if(false){
						alert('Scegliere un valore esistente...');return false;
					}else{
						var url=this.NODEHOST.replace('8069','80')+"/fix_add_to_validator?onload="+encodeURIComponent('window.FIXER._FIX_ADD_TO_VALIDATOR');
						url=url+'&validator_id='+validator_id;
						url=url+'&value='+urlencodedvalue;
						url=url+'&result_value='+encodeURIComponent(chosen);
						console.log((window.FOUNDAREAS||[]).join('**'));
						// url=url+'&areas='+encodeURIComponent((window.FOUNDAREAS||[]).join('**'));
					}
				}else{
					var url=this.NODEHOST.replace('8069','80')+"/fix_add_to_validator?type=newreq&onload="+encodeURIComponent('window.FIXER._FIX_ADD_TO_VALIDATOR');
						url=url+'&validator_id='+validator_id;
						url=url+'&set='+(window.CURRENT_SET||it3.querystring('id',document.location.href.replace('web#','web?')));
						url=url+'&value='+urlencodedvalue;
						console.log((window.FOUNDAREAS||[]).join('**'));
						// url=url+'&areas='+encodeURIComponent((window.FOUNDAREAS||[]).join('**'));
				}
				console.log(url);
				it3.ins(document.head,'script',['src',url]);
				let error_row=ev.target.parentElement.parentElement;
				error_row.parentElement.removeChild(error_row);
				return false;
			},
			_FIX_ADD_TO_VALIDATOR:function(data){console.log(data);}
		}}
		
		window.FIXER.init(data);
	});
// it3.ins(document.head,'script',['src',document.location.protocol+'//'+document.location.host.replace('odoo.','')+'/fapi/config/get_config?savein='+encodeURIComponent('window.FIXER.CONFIG')])