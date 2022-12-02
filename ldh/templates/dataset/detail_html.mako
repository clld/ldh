<%inherit file="../home_comp.mako"/>

<%def name="sidebar()">
    <div class="well">
        <h3>Quick Links</h3>
        <ul>
            <li><a href="${req.route_url('about', _anchor='objectives')}"><strong>Objectives of LDH</strong></a></li>
            <li><a href="${req.route_url('about', _anchor='repository')}"><strong>Structure of LDH/Publication
                Repository</strong></a></li>
            ##<li><a title="Go to page: for authors" href="/for-authors/"><strong>Information for Authors</strong></a></li>
            ##<li><strong><a href="http://ldh.clld.org/for-authors/permission-form/">Download permission form</a></strong></li>
        </ul>
    </div>
</%def>

<h2>Language Description Heritage</h2>
<h3 class="subtitle">an OPEN ACCESS DIGITAL LIBRARY</h3>

<p>The <a title="Go to page: objectives" href="${req.route_url('about')}">goal</a> of the Language
    Description Heritage (LDH) Open Access Library is to provide easy access to descriptive material about the
    world’s languages. This collection is being compiled at the
    ${h.external_link("https://www.eva.mpg.de/", label='Max Planck Institute for Evolutionary Anthropology')}
    in Germany as an open access collection of existing scientific contributions
    describing the world-wide linguistic diversity, focussing on traditionally difficult to obtain works.</p>
<p>More information about the scientific goals of this project is available in the section describing the <a
        title="Go to page: objectives" href="${req.route_url('about', _anchor='objectives')}">objectives</a>
    and details about the open access licensing can
    be found in the section <a title="Go to page: for authors" href="${req.route_url('help')}">for authors</a>.</p>
<p>The scientific contributions that are available in the Language Description Heritage library are stored in the <a
        title="about: repository" href="${req.route_url('about', _anchor='repository')}">publication repository</a>
    of the Max Planck Society or on Zenodo. These
    repositories assures the longevity and stability of the resources. Technically speaking, the website that you are
    currently looking at is only an announcement platform to enhance the visibility of your work.</p>
