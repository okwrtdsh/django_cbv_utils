class RequiredMixin(object):
    multiple_required_list = []
    chain_required_list = []

    def get_multiple_required_list(self):
        return self.multiple_required_list

    def get_chain_required_list(self):
        return self.chain_required_list

    def multiple_required(
            self, cleaned_data, fields,
            func=lambda l: not any(l), msg=None):
        """
        複数の入力による必須項目の判定
        defaultはいずれか必須
        """
        if msg is None:
            msg = "{}のいずれかの入力が必須です。".format(
                "、".join(self.fields[f].label for f in fields))
        cleaned_fields = (cleaned_data.get(f) for f in fields)
        if func(cleaned_fields):
            for f in fields:
                self.add_error(f, msg)

    def chain_required(
        self, cleaned_data, trigger, fields,
            func=bool, msg=None):
        """
        triggerが条件を満たす場合に入力を必須にする
        """
        if msg is None:
            msg = "このフィールドは必須です。"
        if isinstance(trigger, (list, tuple)):
            cleaned_trigger = (cleaned_data.get(f) for f in trigger)
        else:
            cleaned_trigger = cleaned_data.get(trigger)
        if func(cleaned_trigger):
            for f in fields:
                if not cleaned_data.get(f):
                    self.add_error(f, msg)

    def clean(self):
        cleaned_data = super().clean()
        for kwargs in self.get_multiple_required_list():
            self.multiple_required(cleaned_data, **kwargs)
        for kwargs in self.get_chain_required_list():
            self.chain_required(cleaned_data, **kwargs)
        return cleaned_data
