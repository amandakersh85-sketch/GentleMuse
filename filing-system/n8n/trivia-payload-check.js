// The check the n8n Code node runs on every call to daily-trivia-trigger.
//
// Do not paste this into n8n by hand. gm_trivia_trigger.py --workflow --write
// builds daily-trivia-trigger.json from this file and puts RULES above it,
// filled from the data the sender reads: the lane and the 2 minimum lengths
// from gm_trivia_bank.py, the platforms, accounts and calls to action from
// channel-rules.csv, the voice and the 2 avatar looks from the sender. The
// sender and the webhook cannot disagree, because there is 1 copy of each.
//
// Why the webhook checks at all when the sender already has. The webhook
// answers anything that holds the key: the sender, a cron service, a form, a
// curl line pasted from a chat. The design this lane was handed on 09/28 sent
// a free topic, "World History - Forgotten Inventions", for a model to write
// about. This refuses that at the door, whoever sends it.

function checkPayload(body, rules, today) {
  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    return verdict('', ['the body is not a JSON object. Send 1 fact as JSON, Content-Type application/json.']);
  }
  const reasons = [];
  const text = (key) => (typeof body[key] === 'string' ? body[key].trim() : '');

  const factId = text('fact_id');
  if (!new RegExp(rules.factIdPattern).test(factId)) {
    reasons.push('no fact_id from trivia-fact-bank.csv. This trigger carries a checked fact, never a topic. ' +
      'Asked to write about a topic, a model supplies the numbers itself, and those numbers are the whole risk.');
  }
  if (!rules.topics.includes(text('topic'))) {
    reasons.push('topic "' + (text('topic') || '(blank)') + '" is outside the lane, which is ' +
      rules.topics.join(', ') + '. General trivia fills the slot and dilutes what the account is for.');
  }
  if (text('fact').length < rules.minFact) {
    reasons.push('no fact line to write from.');
  }
  if (text('backbone').length < rules.minBackbone) {
    reasons.push('no backbone, so it is trivia with no turn.');
  }
  if (!/^https?:\/\//i.test(text('source_url'))) {
    reasons.push('no source_url, so nobody can check it in 1 click.');
  }
  if (!isDay(text('verified_on'))) {
    reasons.push('no verified_on date, so nothing says a person read the source.');
  }
  if (!rules.delivery.includes(text('delivery'))) {
    reasons.push('delivery "' + (text('delivery') || '(blank)') + '" is not rendered here. This workflow renders ' +
      rules.delivery.join(', ') + ' through HeyGen. motion-text goes through the reel factory.');
  }

  const channels = Object.keys(rules.platforms);
  const platforms = body.target_platform;
  if (!Array.isArray(platforms) || platforms.length === 0) {
    reasons.push('target_platform must be a list drawn from ' + channels.join(', ') + '.');
  } else {
    const seen = {};
    platforms.forEach((name) => {
      const rule = rules.platforms[name];
      if (!rule) {
        const content = rules.notInLane[name];
        const lower = String(name).toLowerCase();
        if (content === undefined && rules.platforms[lower]) {
          reasons.push('"' + name + '" is written ' + lower + ' here.');
        } else {
          reasons.push('"' + name + '" does not carry this lane. ' + (content !== undefined
            ? 'channel-rules.csv has it as: ' + content + '.'
            : 'The channels that do are ' + channels.join(', ') + '.'));
        }
        return;
      }
      if (seen[name]) {
        reasons.push('"' + name + '" is listed twice.');
        return;
      }
      seen[name] = true;
      const account = String((body.accounts || {})[name] || '');
      if (account !== rule.account) {
        reasons.push(name + ' goes to account ' + rule.account + ', not "' + account +
          '". Cesa\'s accounts never carry this lane.');
      }
      const cta = (body.cta || {})[name] || {};
      if (cta.shape !== rule.cta) {
        reasons.push(name + ' call to action is ' + rule.cta + ', not "' + (cta.shape || '(blank)') + '".');
      } else if (rule.cta === 'comment-keyword' && !/^[A-Z][A-Z0-9]{2,15}$/.test(cta.keyword || '')) {
        reasons.push(name + ' asks for a comment keyword and names none.');
      }
      if (rule.cta !== 'comment-keyword' && cta.keyword) {
        reasons.push(name + ' never carries the comment keyword. Nothing there answers it, ' +
          'and a dead keyword is worse than none.');
      }
      if (rule.cta === 'link-in-description' && !/^https?:\/\//i.test(cta.link || '')) {
        reasons.push(name + ' needs the link that goes in the description.');
      }
    });
  }

  if (body.voice_id !== rules.voiceId) {
    reasons.push('voice_id is not Amanda\'s voice. Avery and Cesa are separate people with separate voices, ' +
      'and this lane speaks as her.');
  }
  if (!rules.avatarIds.includes(body.avatar_id)) {
    reasons.push('avatar_id is not 1 of her 2 podcast looks.');
  }

  const day = text('publish_date');
  if (!isDay(day)) {
    reasons.push('publish_date must be the day, YYYY-MM-DD. Each platform\'s time comes from its slot ' +
      'when it is scheduled, after Amanda approves.');
  } else if (day < today) {
    reasons.push('publish_date ' + day + ' is already past.');
  }

  return verdict(factId, reasons);
}

function verdict(factId, reasons) {
  return {ok: reasons.length === 0, status: reasons.length === 0 ? 202 : 422, fact_id: factId, reasons: reasons};
}

function isDay(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value || '')) return false;
  const d = new Date(value + 'T00:00:00Z');
  return !isNaN(d.getTime()) && d.toISOString().slice(0, 10) === value;
}

function todayIn(timeZone) {
  // en-CA writes a date as YYYY-MM-DD.
  return new Intl.DateTimeFormat('en-CA', {timeZone: timeZone, year: 'numeric', month: '2-digit', day: '2-digit'})
    .format(new Date());
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {checkPayload, isDay, todayIn};
}
