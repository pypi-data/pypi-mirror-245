{% macro new_section(changes, title) -%}
{%- if changes %}
### {{ title }}

{% for change in changes|sort(attribute="fulltitle") -%}
- {% if change.breaking_change %}*BREAKING CHANGE* {% endif %}{{ change.fulltitle }}{% if change.issue %} ({{ change.issue }}){% endif %}
{% endfor -%}

{%- endif %}
{%- endmacro -%}

## Version {{ changelog.version }} ({{ date.today().isoformat() }})
{{- new_section(changelog.changes[ChangeType.feat], "🎉 New features") }}
{{- new_section(changelog.changes[ChangeType.perf], "🚀 Performance improvements") }}
{{- new_section(changelog.changes[ChangeType.fix], "👷 Bug fixes") }}
{{- new_section(changelog.changes[ChangeType.docs], "📝 Documentation") }}
{{- new_section(changelog.changes[ChangeType.ci], "🤖 Continuous integration") }}
{{- new_section(changelog.changes[ChangeType.unknown], "🤷 Various changes") }}
