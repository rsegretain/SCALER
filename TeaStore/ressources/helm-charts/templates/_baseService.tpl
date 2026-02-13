{{- define "teastore.templates.baseService" }}
apiVersion: v1
kind: Service
metadata:
  name: {{ .Values.global.name }}-{{ .Chart.Name }}
  labels:
    app: {{ .Values.global.appLabel }}
    run: {{ .Values.global.name }}-{{ .Chart.Name }}
spec:
  {{- if .Values.serviceType }}
  type: {{ .Values.serviceType }}
  {{- end}}
  ports:
  - port: {{ .Values.container.port }}
    {{- if .Values.nodePort }}
    nodePort: {{ .Values.nodePort }}
    {{- end}}
    protocol: TCP
  selector:
    run: {{ .Values.global.name }}-{{ .Chart.Name }}
{{- end}}