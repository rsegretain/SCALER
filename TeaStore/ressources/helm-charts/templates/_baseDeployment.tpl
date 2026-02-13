{{- define "teastore.templates.baseDeployment" }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Values.global.name }}-{{ .Chart.Name }}
  labels:
    app: {{ .Values.global.appLabel }}
    run: {{ .Values.global.name }}-{{ .Chart.Name }}
spec:
  {{- if .Values.progressDeadlineSeconds }}
  progressDeadlineSeconds: {{ .Values.progressDeadlineSeconds }}
  {{- end}}
  selector:
    matchLabels:
      app: {{ .Values.global.appLabel }}
      run: {{ .Values.global.name }}-{{ .Chart.Name }}
  template:
    metadata:
      annotations:
        sidecar.istio.io/statsHistogramBuckets: '{"istiocustom":[50,100,200,500,1000,2500,5000,10000]}'
      labels:
        app: {{ .Values.global.appLabel }}
        run: {{ .Values.global.name }}-{{ .Chart.Name }}
    spec:
      containers:
      - name: {{ .Values.global.name }}-{{ .Chart.Name }}
        image: {{ .Values.global.containerRegistry }}/{{ .Values.container.image }}
        ports:
        - containerPort: {{ .Values.container.port }}
        {{- if .Values.container.env }}
        env:
        {{- range $e := .Values.container.env }}
        - name: {{ $e.name }}
          value: "{{ $e.value | toString }}"
        {{- end }}
        {{- end }}
        resources:
          limits:
            {{- if or .Values.container.cpu .Values.global.cpu }}
            cpu: {{ .Values.container.cpu | default .Values.global.cpu | quote }}
            {{- end }}
            {{- if or .Values.container.memory .Values.global.memory }}
            memory: {{ .Values.container.memory | default .Values.global.memory | quote }}
            {{- end }}
        {{- if .Values.container.startupProbe }}
        startupProbe:
          httpGet:
            path: {{ .Values.container.startupProbe.endpoint }}
            port: {{ .Values.container.port }}
          initialDelaySeconds: {{ .Values.container.startupProbe.initialDelaySeconds | default .Values.global.startupProbe.initialDelaySeconds}}
          failureThreshold: {{ .Values.container.startupProbe.failureThreshold | default .Values.global.startupProbe.failureThreshold }}
          periodSeconds: {{ .Values.container.startupProbe.periodSeconds | default .Values.global.startupProbe.periodSeconds }}
        {{- end}}
      imagePullSecrets:
        - name: {{ .Values.global.imagePullSecretsName }}
{{- end}}