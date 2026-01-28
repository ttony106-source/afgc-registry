// Cloudflare Pages Function for lead capture
// POST /api/lead

interface Env {
  TURNSTILE_SECRET_KEY: string;
  LEAD_WEBHOOK_URL: string;
}

interface LeadData {
  name: string;
  email: string;
  company?: string;
  message?: string;
  turnstileToken: string;
}

export const onRequestPost: PagesFunction<Env> = async (context) => {
  const { request, env } = context;

  try {
    const data: LeadData = await request.json();

    // Validate required fields
    if (!data.name || !data.email || !data.turnstileToken) {
      return new Response(
        JSON.stringify({ error: 'Missing required fields' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Verify Turnstile token
    const turnstileResponse = await fetch(
      'https://challenges.cloudflare.com/turnstile/v0/siteverify',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          secret: env.TURNSTILE_SECRET_KEY,
          response: data.turnstileToken,
          remoteip: request.headers.get('CF-Connecting-IP') || '',
        }),
      }
    );

    const turnstileResult = await turnstileResponse.json() as { success: boolean };

    if (!turnstileResult.success) {
      return new Response(
        JSON.stringify({ error: 'Turnstile verification failed' }),
        { status: 403, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Forward to webhook (Make/Zapier)
    if (env.LEAD_WEBHOOK_URL) {
      await fetch(env.LEAD_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: data.name,
          email: data.email,
          company: data.company || '',
          message: data.message || '',
          timestamp: new Date().toISOString(),
          source: 'afgc-registry-site',
        }),
      });
    }

    return new Response(
      JSON.stringify({ success: true, message: 'Lead submitted successfully' }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    console.error('Lead submission error:', error);
    return new Response(
      JSON.stringify({ error: 'Internal server error' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};
