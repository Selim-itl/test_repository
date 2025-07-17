odoo.define('itl_it_ticketing.helpdesk_dashboard_action', function (require){
"use strict";
var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var rpc = require('web.rpc');
var ajax = require('web.ajax');
var CustomDashBoard = AbstractAction.extend({
   template: 'ItlBdItTicketingDashBoard',

   start: function() {
        var self = this;
        ajax.rpc('/helpdesk_dashboard').then(function (res) {
        self.$el.find("#new_state_value").text(res.new)
        self.$el.find("#mis_stage_value").text(res.in_mis)
        self.$el.find("#on_hold_value").text(res.cs)
        self.$el.find("#inprogress_value").text(res.in_progress)
        self.$el.find("#canceled_value").text(res.canceled)
        self.$el.find("#verification_value").text(res.verification)
        self.$el.find("#done_value").text(res.done)
        self.$el.find("#correction_stage_value").text(res.correction)
        self.$el.find("#closed_value").text(res.closed)
//        Update the dashboard new state value
        self.$el.find("#new_state").click(function(){
        self.do_action({
            name:'New Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.new_id]],
        })
        })
//      Update the dashboard in progress state value
        self.$el.find("#in_progress_state").click(function(){
        self.do_action({
            name:'In progress Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.in_progress_id]],
        })
        })
        // Update the dashboard in MIS state value
        self.$el.find("#in_mis_state").click(function(){
        self.do_action({
            name:'MIS Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.in_mis_id]],
        })
        })

        // Update the dashboard in On Hold state value
        self.$el.find("#on_hold_state").click(function(){
        self.do_action({
            name:'On Hold Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.cs_id]],
        })
        })

//         Update the dashboard cancel state value
        self.$el.find("#cancelled_state").click(function(){
        self.do_action({
            name:'Canceled Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.canceled_id]],
        })
        })
//         Update the dashboard verification state value
        self.$el.find("#verification_state").click(function(){
        self.do_action({
            name:'Verification Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.verification_id]],
        })
        })
        // Update filtering Correction state update
        self.$el.find("#correction_state").click(function(){
        self.do_action({
            name:'Correction Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.correction_id]],
        })
        })

//         Update the dashboard done state value
        self.$el.find("#done_state").click(function(){
        self.do_action({
            name:'Done Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.done_id]],
        })
        })
//         Update the dashboard closed state value
        self.$el.find("#closed_state").click(function(){
        self.do_action({
            name:'Closed Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.closed_id]],
        })
        })
//        week function start
        self.$el.find("#filter_selection").change(function(e){
        var target = $(e.target)
        var value = target.val()
        if (value == "this_week") {
        ajax.rpc('/helpdesk_dashboard_week').then(function (res) {
        self.$el.find("#new_state_value").text(res.new)
        self.$el.find("#mis_stage_value").text(res.in_mis)
        self.$el.find("#on_hold_value").text(res.cs)
        self.$el.find("#inprogress_value").text(res.in_progress)
        self.$el.find("#canceled_value").text(res.canceled)
        self.$el.find("#verification_value").text(res.verification)
        self.$el.find("#done_value").text(res.done)
        self.$el.find("#correction_stage_value").text(res.correction)
        self.$el.find("#closed_value").text(res.closed)
//        Week function new state updation
        self.$el.find("#new_state").click(function(){
        self.do_action({
            name:'New Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.new_id]],
        })
        })
//        Week function in progress state update
        self.$el.find("#in_progress_state").click(function(){
        self.do_action({
            name:'In progress Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.in_progress_id]],
        })
        })
        // Week Update the dashboard in MIS state value
        self.$el.find("#in_mis_state").click(function(){
        self.do_action({
            name:'MIS Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.in_mis_id]],
        })
        })

        // Week Update the dashboard in On Hold state value
        self.$el.find("#on_hold_state").click(function(){
        self.do_action({
            name:'On Hold Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.cs_id]],
        })
        })

        // Week filtering Correction state update
        self.$el.find("#correction_state").click(function(){
        self.do_action({
            name:'Correction Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.correction_id]],
        })
        })

//         Week function in cancel state update
        self.$el.find("#cancelled_state").click(function(){
        self.do_action({
            name:'Canceled Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.canceled_id]],
        })
        })
//     week function in verification state update
        self.$el.find("#verification_state").click(function(){
        self.do_action({
            name:'Verification Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.verification_id]],
        })
        })

//         Week function in done state update
        self.$el.find("#done_state").click(function(){
        self.do_action({
            name:'Done Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.done_id]],
        })
        })
//         Week function in closed state update
        self.$el.find("#closed_state").click(function(){
        self.do_action({
            name:'Closed Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.closed_id]],
             })
          })
        })
        }
//        Month function start
        else if (value == "this_month") {
        ajax.rpc('/helpdesk_dashboard_month').then(function (res) {
        self.$el.find("#new_state_value").text(res.new)
        self.$el.find("#mis_stage_value").text(res.in_mis)
        self.$el.find("#on_hold_value").text(res.cs)
        self.$el.find("#inprogress_value").text(res.in_progress)
        self.$el.find("#canceled_value").text(res.canceled)
        self.$el.find("#verification_value").text(res.verification)
        self.$el.find("#done_value").text(res.done)
        self.$el.find("#correction_stage_value").text(res.correction)
        self.$el.find("#closed_value").text(res.closed)
//        Month searching new state update
        self.$el.find("#new_state").click(function(){
        self.do_action({
            name:'New Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.new_id]],
        })
        })
//        Month searching in progress state update
        self.$el.find("#in_progress_state").click(function(){
        self.do_action({
            name:'In progress Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.in_progress_id]],
        })
        })
        // Month Update the dashboard in MIS state value
        self.$el.find("#in_mis_state").click(function(){
        self.do_action({
            name:'MIS Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.in_mis_id]],
        })
        })

        // Month the dashboard in On Hold state value
        self.$el.find("#on_hold_state").click(function(){
        self.do_action({
            name:'On Hold Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.cs_id]],
        })
        })
//        Month searching cancel state update
        self.$el.find("#cancelled_state").click(function(){
        self.do_action({
            name:'Canceled Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.canceled_id]],
        })
        })
//         Month Verification state update
        self.$el.find("#verification_state").click(function(){
        self.do_action({
            name:'Verification Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.verification_id]],
        })
        })

        // Month filtering Correction state update
        self.$el.find("#correction_state").click(function(){
        self.do_action({
            name:'Correction Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.correction_id]],
        })
        })

//        Month searching done state update
        self.$el.find("#done_state").click(function(){
        self.do_action({
            name:'Done Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.done_id]],
        })
        })
//        Month searching closed state update
        self.$el.find("#closed_state").click(function(){
        self.do_action({
            name:'Closed Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.closed_id]],
             })
          })
          })
        }
//        Year filtering start -----------
        else if (value == "this_year") {
        ajax.rpc('/helpdesk_dashboard_year').then(function (res) {
             self.$el.find("#new_state_value").text(res.new)
        self.$el.find("#mis_stage_value").text(res.in_mis)
        self.$el.find("#on_hold_value").text(res.cs)
        self.$el.find("#inprogress_value").text(res.in_progress)
        self.$el.find("#canceled_value").text(res.canceled)
        self.$el.find("#verification_value").text(res.verification)
        self.$el.find("#done_value").text(res.done)
        self.$el.find("#correction_stage_value").text(res.correction)
        self.$el.find("#closed_value").text(res.closed)
//        Year filtering new state update
        self.$el.find("#new_state").click(function(){
        self.do_action({
            name:'New Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.new_id]],
        })
        })
//        Year filtering in progress state update
        self.$el.find("#in_progress_state").click(function(){
        self.do_action({
            name:'In progress Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.in_progress_id]],
        })
        })

        // Year filtering the dashboard in MIS state value
        self.$el.find("#in_mis_state").click(function(){
        self.do_action({
            name:'MIS Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.in_mis_id]],
        })
        })

        // Year Update the dashboard in On Hold state value
        self.$el.find("#on_hold_state").click(function(){
        self.do_action({
            name:'On Hold Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.cs_id]],
        })
        })
//        Year filtering cancel state update
        self.$el.find("#cancelled_state").click(function(){
        self.do_action({
            name:'Canceled Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.canceled_id]],
        })
        })
//         Year Verification state update
        self.$el.find("#verification_state").click(function(){
        self.do_action({
            name:'Verification Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.verification_id]],
        })
        })

        // Year filtering Correction state update
        self.$el.find("#correction_state").click(function(){
        self.do_action({
            name:'Correction Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.correction_id]],
        })
        })

//        Year filtering done state update
        self.$el.find("#done_state").click(function(){
        self.do_action({
            name:'Done Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.done_id]],
        })
        })
//        Year filtering closed state update
        self.$el.find("#closed_state").click(function(){
        self.do_action({
            name:'Closed Tickets',
            type: 'ir.actions.act_window',
            res_model: 'it.itl.bd.help.ticket',
            view_mode: 'tree,form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['id', '=', res.closed_id]],
             })
          })
          })
        }
        });
   })
  },
})
core.action_registry.add('helpdesk_dashboard_tag', CustomDashBoard);
return CustomDashBoard
})
