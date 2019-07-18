<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Language')} ${ctx.name}</h2>

<h3>Descriptions</h3>
<ul>
    % for d in ctx.descriptions:
        <li>
            ${h.link(request, d)}: ${h.link(request, d, label=d.description)}
        </li>
    % endfor
</ul>

<%def name="sidebar()">
    ${util.codes()}
   <div style="clear: right;"> </div>

    <div class="well-small well">
        ${request.map.render()}
        ${h.format_coordinates(ctx)}
    </div>
</%def>
