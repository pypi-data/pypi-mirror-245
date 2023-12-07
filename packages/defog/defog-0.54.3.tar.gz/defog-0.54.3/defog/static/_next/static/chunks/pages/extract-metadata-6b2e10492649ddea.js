(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[99],{97362:function(e,t,a){(window.__NEXT_P=window.__NEXT_P||[]).push(["/extract-metadata",function(){return a(71166)}])},4278:function(e,t,a){"use strict";var s=a(85893),l=a(9008),n=a.n(l);let i=()=>(0,s.jsxs)(n(),{children:[(0,s.jsx)("title",{children:"Defog.ai - AI Assistant for Data Analysis"}),(0,s.jsx)("meta",{name:"description",content:"Train your AI data assistant on your own device"}),(0,s.jsx)("meta",{name:"viewport",content:"width=device-width, initial-scale=1"}),(0,s.jsx)("link",{rel:"icon",href:"/favicon.ico"})]});t.Z=i},35175:function(e,t,a){"use strict";var s=a(85893);a(67294);var l=a(69215);let n=e=>{let{id:t,children:a}=e,{Content:n,Sider:i}=l.Ar,d=[{key:"select-model",title:"Select Model",icon:(0,s.jsx)("a",{href:"/",children:"1. Select Model"})},{key:"extract-metadata",title:"Extract Metadata",icon:(0,s.jsx)("a",{href:"/extract-metadata",children:"2. Extract Metadata"})},{key:"instruct-model",title:"Instruct Model",icon:(0,s.jsx)("a",{href:"/instruct-model",children:"3. Instruct Model"})},{key:"query-database",title:"Query your database",icon:(0,s.jsx)("a",{href:"/query-database",children:"4. Query Database"})}];return(0,s.jsx)(l.Ar,{style:{height:"100vh"},children:(0,s.jsxs)(n,{style:{padding:"50 50"},children:[(0,s.jsx)(i,{style:{height:"100vh",position:"fixed"},children:(0,s.jsx)(l.v2,{style:{width:200,paddingTop:"2em",paddingBottom:"2em"},mode:"inline",selectedKeys:[t],items:d})}),(0,s.jsx)("div",{style:{paddingLeft:240,paddingTop:30},children:a})]})})};t.Z=n},71166:function(e,t,a){"use strict";a.r(t);var s=a(85893),l=a(67294),n=a(4278),i=a(35175),d=a(69215);let o=()=>{let{Option:e}=d.Ph,[t,a]=(0,l.useState)({}),[o,r]=(0,l.useState)([]),[c,h]=(0,l.useState)(!1),[m,p]=(0,l.useState)([]),[x,u]=(0,l.useState)("");return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(n.Z,{}),(0,s.jsxs)(i.Z,{id:"extract-metadata",children:[(0,s.jsx)("h1",{style:{paddingBottom:"1em"},children:"Extract Metadata"}),(0,s.jsxs)(d.X2,{type:"flex",height:"100vh",children:[(0,s.jsx)(d.JX,{md:{span:8},xs:{span:24},children:(0,s.jsxs)("div",{children:[(0,s.jsxs)(d.l0,{name:"db_creds",labelCol:{span:8},wrapperCol:{span:16},style:{maxWidth:400},disabled:c,onFinish:async e=>{a(e);let t=await fetch("http://localhost:8000/get_tables",{method:"POST",body:JSON.stringify(e)}),s=await t.json();r(s.tables)},children:[(0,s.jsx)(d.l0.Item,{name:"db_type",label:(0,s.jsxs)("div",{children:["Database Type ",(0,s.jsx)(d.u,{title:"only postgres is supported on the community model",children:"ℹ"})]}),children:(0,s.jsxs)(d.Ph,{style:{width:"100%"},initialValue:"postgres",children:[(0,s.jsx)(e,{value:"postgres",children:"PostgreSQL"}),(0,s.jsx)(e,{value:"mysql",disabled:!0,children:"MySQL"}),(0,s.jsx)(e,{value:"snowflake",disabled:!0,children:"Snowflake"}),(0,s.jsx)(e,{value:"redshift",disabled:!0,children:"Redshift"}),(0,s.jsx)(e,{value:"bigquery",disabled:!0,children:"BigQuery"})]})}),(0,s.jsx)(d.l0.Item,{label:"Database Host",name:"host",initialValue:"localhost",children:(0,s.jsx)(d.II,{style:{width:"100%"}})}),(0,s.jsx)(d.l0.Item,{name:"port",label:"Database Port",initialValue:"5432",children:(0,s.jsx)(d.II,{style:{width:"100%"}})}),(0,s.jsx)(d.l0.Item,{name:"username",label:"DB Username",initialValue:"postgres",children:(0,s.jsx)(d.II,{style:{width:"100%"}})}),(0,s.jsx)(d.l0.Item,{name:"password",label:"DB Password",initialValue:"postgres",children:(0,s.jsx)(d.II,{style:{width:"100%"}})}),(0,s.jsx)(d.l0.Item,{name:"database",label:"DB Name",initialValue:"postgres",children:(0,s.jsx)(d.II,{style:{width:"100%"}})}),(0,s.jsx)(d.l0.Item,{wrapperCol:{span:24},children:(0,s.jsx)(d.zx,{type:"primary",style:{width:"100%"},htmlType:"submit",children:"Get Tables"})})]}),o.length>0&&(0,s.jsxs)(d.l0,{name:"db_tables",labelCol:{span:8},wrapperCol:{span:16},style:{maxWidth:400},disabled:c,onFinish:async e=>{h(!0);let a=await fetch("http://localhost:8000/get_metadata",{method:"POST",body:JSON.stringify({...t,tables:e.tables})}),s=await a.json();h(!1),p(s.schema)},children:[(0,s.jsx)(d.l0.Item,{name:"tables",label:"Tables to index",children:(0,s.jsx)(d.Ph,{mode:"multiple",style:{width:"100%",maxWidth:400},children:o.map(t=>(0,s.jsx)(e,{value:t,children:t}))})}),(0,s.jsx)(d.l0.Item,{wrapperCol:{span:24},children:(0,s.jsx)(d.zx,{type:"primary",style:{width:"100%",maxWidth:535},htmlType:"submit",children:"Extract Metadata"})})]})]})}),(0,s.jsxs)(d.JX,{md:{span:16},xs:{span:24},style:{paddingRight:"2em",height:600,overflowY:"scroll"},children:[m.length>0&&(0,s.jsx)(d.zx,{type:"primary",style:{width:"100%",maxWidth:535},disabled:c,loading:c,onClick:async()=>{h(!0);let e=await fetch("http://localhost:8000/update_metadata",{method:"POST",body:JSON.stringify({metadata:m,allowed_joins:x})}),t=await e.json();console.log(t),h(!1),void 0!==t.suggested_joins&&null!==t.suggested_joins&&""!==t.suggested_joins&&(console.log("Here!"),u(t.suggested_joins),document.getElementById("allowed-joins").value=t.suggested_joins),d.yw.success("Metadata updated successfully!")},children:"Update metadata on server"}),m.length>0?(0,s.jsxs)(d.X2,{style:{marginTop:"1em",position:"sticky",top:0,paddingBottom:"1em",paddingTop:"1em",backgroundColor:"white",zIndex:100},children:[(0,s.jsx)(d.JX,{xs:{span:24},md:{span:4},style:{overflowWrap:"break-word"},children:(0,s.jsx)("b",{children:"Table Name"})}),(0,s.jsx)(d.JX,{xs:{span:24},md:{span:4},style:{overflowWrap:"break-word"},children:(0,s.jsx)("b",{children:"Column Name"})}),(0,s.jsx)(d.JX,{xs:{span:24},md:{span:4},style:{overflowWrap:"break-word"},children:(0,s.jsx)("b",{children:"Data Type"})}),(0,s.jsx)(d.JX,{xs:{span:24},md:{span:12},children:(0,s.jsx)("b",{children:"Description (Optional)"})})]}):null,m.length>0&&m.map((e,t)=>(0,s.jsxs)(d.X2,{style:{marginTop:"1em"},children:[(0,s.jsx)(d.JX,{xs:{span:24},md:{span:4},style:{overflowWrap:"break-word"},children:e.table_name}),(0,s.jsx)(d.JX,{xs:{span:24},md:{span:4},style:{overflowWrap:"break-word"},children:e.column_name}),(0,s.jsx)(d.JX,{xs:{span:24},md:{span:4},style:{overflowWrap:"break-word"},children:e.data_type}),(0,s.jsx)(d.JX,{xs:{span:24},md:{span:12},children:(0,s.jsx)(d.II.TextArea,{placeholder:"Description of what this column does",initialValue:e.column_description,autoSize:{minRows:2},onKeyDown:async t=>{if("Enter"===t.key&&t.metaKey){let a=await fetch("http://localhost:8000/make_gguf_request",{method:"POST",body:JSON.stringify({prompt:"# Task\nAdd a column description for the following column inside a SQL table. Only return the column description and nothing else.\n\n# Schema\nTable Name: ".concat(e.table_name,"\nColumn Name: ").concat(e.column_name,"\nData Type: ").concat(e.data_type,"\nColumn Description:")})}),s=await a.json(),l=s.completion;t.target.value=l}},onChange:e=>{let a=[...m];a[t].column_description=e.target.value,p(a)}},t)})]},t)),m.length>0?(0,s.jsx)(d.X2,{children:(0,s.jsxs)(d.JX,{span:24,children:[(0,s.jsx)("h2",{style:{paddingTop:"1em"},children:"Allowed Joins"}),(0,s.jsx)(d.II.TextArea,{id:"allowed-joins",placeholder:"Allowed Joins",initialValue:x,autoSize:{minRows:2},value:x,onChange:e=>{u(e.target.value)}})]})}):null]})]})]})]})};t.default=o}},function(e){e.O(0,[215,774,888,179],function(){return e(e.s=97362)}),_N_E=e.O()}]);