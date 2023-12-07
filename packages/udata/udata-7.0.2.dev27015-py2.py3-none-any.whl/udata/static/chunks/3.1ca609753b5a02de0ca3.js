webpackJsonp([3,31],{345:function(t,e,s){var o,i;s(1643),o=s(1417),i=s(1519),t.exports=o||{},t.exports.__esModule&&(t.exports=t.exports.default),i&&(("function"==typeof t.exports?t.exports.options||(t.exports.options={}):t.exports).template=i)},1417:function(t,e,s){"use strict";function _interopRequireDefault(t){return t&&t.__esModule?t:{default:t}}Object.defineProperty(e,"__esModule",{value:!0});var o=s(99),i=_interopRequireDefault(o),n=s(57),d=(_interopRequireDefault(n),s(318)),c=_interopRequireDefault(d),a=s(323),l=_interopRequireDefault(a),r=s(325),u=_interopRequireDefault(r);e.default={name:"discussion-modal",components:{Modal:c.default,DatasetCard:l.default,ReuseCard:u.default},computed:{title:function(){return this.deleting?this._("Confirm deletion"):this._("Discussion")},formValid:function(){return this.comment&&this.comment.length>0}},data:function(){return{discussion:{},next_route:null,comment:null,deleting:!1}},events:{"modal:closed":function(){this.$go(this.next_route)}},route:{data:function(){var t=this;if(this.$route.matched.length>1){var e=this.$route.matched.length-2,s=this.$route.matched[e];this.next_route={name:s.handler.name,params:s.params}}var o=this.$route.params.discussion_id;i.default.discussions.get_discussion({id:o},function(e){t.discussion=e.obj})}},methods:{confirm_delete:function(){this.deleting=!0},cancel_delete:function(){this.deleting=!1},confirm_delete_comment:function(t){var e=this;confirm(this._("Are you sure you want to delete this comment?"))&&i.default.discussions.delete_discussion_comment({id:this.discussion.id,cidx:t},function(s){e.discussion.discussion.splice(t,1)},this.$root.handleApiError)},delete:function(){var t=this;i.default.discussions.delete_discussion({id:this.discussion.id},function(e){t.$refs.modal.close()},this.$root.handleApiError)},close_discussion:function(){this.send_comment(this.comment,!0)},comment_discussion:function(){this.send_comment(this.comment)},send_comment:function(t,e){var s=this;this.formValid&&i.default.discussions.comment_discussion({id:this.discussion.id,payload:{comment:t,close:e||!1}},function(t){s.discussion=t.obj,s.comment=null},this.$root.handleApiError)}}}},1492:function(t,e,s){e=t.exports=s(37)(),e.push([t.id,".discussion-modal h3{margin-top:0}.discussion-modal .direct-chat-messages{height:auto}.discussion-modal .direct-chat-delete{padding-left:10px;text-decoration:underline;color:#fff}.discussion-modal .direct-chat-timestamp{color:#eee}.discussion-modal .direct-chat-text{background:#fff;border:1px solid #fff}.discussion-modal .direct-chat-text:after,.discussion-modal .direct-chat-text:before{border-right-color:#fff}.discussion-modal .card-container{margin-bottom:1em}","",{version:3,sources:["/./js/components/discussions/modal.vue"],names:[],mappings:"AAAA,qBAAqB,YAAY,CAAC,wCAAwC,WAAW,CAAC,sCAAsC,kBAAkB,0BAA0B,UAAW,CAAC,yCAAyC,UAAU,CAAC,oCAAoC,gBAAgB,qBAAqB,CAAC,qFAAqF,uBAAuB,CAAC,kCAAkC,iBAAiB,CAAC",file:"modal.vue",sourcesContent:[".discussion-modal h3{margin-top:0}.discussion-modal .direct-chat-messages{height:auto}.discussion-modal .direct-chat-delete{padding-left:10px;text-decoration:underline;color:white}.discussion-modal .direct-chat-timestamp{color:#eee}.discussion-modal .direct-chat-text{background:#fff;border:1px solid #fff}.discussion-modal .direct-chat-text:before,.discussion-modal .direct-chat-text:after{border-right-color:#fff}.discussion-modal .card-container{margin-bottom:1em}"],sourceRoot:"webpack://"}])},1519:function(t,e){t.exports=' <modal v-ref:modal :title=title class=discussion-modal :large=!deleting :class="{\'modal-danger\': deleting, \'modal-info\': !deleting}"> <div class=modal-body v-show=!deleting> <div class="row card-container"> <dataset-card class="col-xs-12 col-md-offset-3 col-md-6" v-if="discussion.subject | is \'dataset\'" :datasetid=discussion.subject.id></dataset-card> <reuse-card class="col-xs-12 col-md-offset-3 col-md-6" v-if="discussion.subject | is \'reuse\'" :reuseid=discussion.subject.id></reuse-card> </div> <h3>{{ discussion.title }}</h3> <div class=direct-chat-messages> <div class=direct-chat-msg v-for="(idx, message) in discussion.discussion"> <div class="direct-chat-info clearfix"> <span class="direct-chat-name pull-left">{{message.posted_by | display}}</span> <a v-if="$root.me.is_admin && idx !== 0" @click.prevent=confirm_delete_comment(idx) href class="direct-chat-name direct-chat-delete">{{ _(\'Delete comment\') }}</a> <span class="direct-chat-timestamp pull-right">{{message.posted_on | dt}}</span> </div> <img class=direct-chat-img :alt="_(\'User Image\')" :src="message.posted_by | avatar_url 40"/> <div class=direct-chat-text v-markdown=message.content></div> </div> </div> </div> <div class=modal-body v-show=deleting> <p class="lead text-center"> {{ _(\'You are about to delete this discussion\') }} </p> <p class="lead text-center"> {{ _(\'Are you sure?\') }} </p> </div> <footer class="modal-footer text-center" v-show=!deleting> <form v-if=!discussion.closed v-el:form> <div class=form-group :class="{\'has-success\': formValid}"> <textarea class=form-control rows=3 :placeholder="_(\'Type your comment\')" v-model=comment required>\n                </textarea> </div> </form> <button type=button class="btn btn-info btn-flat pull-left" @click=$refs.modal.close> {{ _(\'Close\') }} </button> <button type=button class="btn btn-danger btn-flat" v-if=$root.me.is_admin @click=confirm_delete> {{ _(\'Delete\') }} </button> <button type=button class="btn btn-outline btn-flat" :disabled=!formValid @click=comment_discussion v-if=!discussion.closed> {{ _(\'Comment the discussion\') }} </button> <button type=button class="btn btn-outline btn-flat" :disabled=!formValid @click=close_discussion v-if=!discussion.closed> {{ _(\'Comment and close discussion\') }} </button> </footer> <footer class="modal-footer text-center" v-show=deleting> <button type=button class="btn btn-danger btn-flat pull-left" @click=cancel_delete> {{ _(\'Cancel\') }} </button> <button type=button class="btn btn-warning btn-flat" @click=delete> {{ _(\'Confirm\') }} </button> </footer> </modal> '},1643:function(t,e,s){var o=s(1492);"string"==typeof o&&(o=[[t.id,o,""]]);s(38)(o,{sourceMap:!0});o.locals&&(t.exports=o.locals)}});
//# sourceMappingURL=3.1ca609753b5a02de0ca3.js.map